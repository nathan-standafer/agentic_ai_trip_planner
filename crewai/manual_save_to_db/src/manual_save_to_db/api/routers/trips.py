"""Trip planning API endpoints."""

import uuid
import json
import asyncio
from typing import Dict, AsyncGenerator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..schemas.trip import TripRequest, TripResponse, TripStatus, ScheduledActivityResponse, UpdateRequest
from ..services.crew_runner import TripPlannerService, PlanUpdaterService

router = APIRouter(prefix="/api/trips", tags=["trips"])

# In-memory store for active planning sessions
# In production, use Redis or database
active_sessions: Dict[str, TripPlannerService] = {}
trip_inputs: Dict[str, dict] = {}  # Store original trip inputs for updates


@router.post("/plan")
async def start_trip_planning(request: TripRequest) -> dict:
    """Start a new trip planning session.

    Returns a trip_id that can be used to stream progress and get results.
    """
    trip_id = str(uuid.uuid4())

    # Convert request to crew inputs format (matching main.py structure)
    inputs = {
        'location': request.destinations,
        'arrival_date': request.arrival_date.isoformat(),
        'departure_date': request.departure_date.isoformat() if request.departure_date else '',
        'trip_considerations': request.other_considerations or '',
        'activity_considerations': request.desired_activities or '',
        'food_considerations': request.food_considerations or '',
    }

    # Store inputs for potential updates
    trip_inputs[trip_id] = inputs

    # Create service and start planning
    service = TripPlannerService(trip_id)
    active_sessions[trip_id] = service
    service.start_planning(inputs)

    return {"trip_id": trip_id, "status": "started"}


async def sse_generator(service: TripPlannerService) -> AsyncGenerator[bytes, None]:
    """Generate SSE formatted events from the service."""
    import sys
    print("sse_generator: starting", file=sys.stderr)
    async for event_data in service.stream_progress():
        # Format as SSE: data: <json>\n\n
        msg = f"data: {event_data}\n\n"
        print(f"sse_generator: sending {len(msg)} bytes", file=sys.stderr)
        yield msg.encode('utf-8')


@router.get("/plan/{trip_id}/stream")
async def stream_progress(trip_id: str):
    """Stream real-time progress updates via Server-Sent Events.

    Connect to this endpoint to receive progress updates as the agents work.
    """
    if trip_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Trip planning session not found")

    service = active_sessions[trip_id]

    return StreamingResponse(
        sse_generator(service),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


@router.get("/plan/{trip_id}/result", response_model=TripResponse)
async def get_result(trip_id: str) -> TripResponse:
    """Get the final trip planning result.

    Call this after the SSE stream completes to get the full itinerary.
    """
    if trip_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Trip planning session not found")

    service = active_sessions[trip_id]

    if service.is_running:
        return TripResponse(
            trip_id=trip_id,
            status=TripStatus.PENDING,
        )

    if service.error:
        return TripResponse(
            trip_id=trip_id,
            status=TripStatus.ERROR,
            error_message=service.error
        )

    # Retrieve schedule from database
    try:
        from manual_save_to_db.tools.db import retrieve_schedule, DB_FILENAME
        import sys
        print(f"Retrieving schedule from database: {DB_FILENAME}", file=sys.stderr)
        schedule_items = retrieve_schedule()
        print(f"Retrieved {len(schedule_items)} scheduled activities", file=sys.stderr)
        schedule = [
            ScheduledActivityResponse(
                date=item.date,
                time_slot=item.time_slot,
                activity_name=item.activity_name,
                activity_description=item.activity_description,
                location=item.location,
                duration=item.duration,
                transportation=item.transportation,
                notes=item.notes
            )
            for item in schedule_items
        ]
    except Exception as e:
        import sys
        import traceback
        print(f"Error retrieving schedule: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        schedule = []

    return TripResponse(
        trip_id=trip_id,
        status=TripStatus.COMPLETED,
        result=service.result,
        schedule=schedule
    )


@router.delete("/plan/{trip_id}")
async def cleanup_session(trip_id: str) -> dict:
    """Clean up a planning session."""
    if trip_id in active_sessions:
        del active_sessions[trip_id]
    if trip_id in trip_inputs:
        del trip_inputs[trip_id]
    return {"status": "cleaned", "trip_id": trip_id}


@router.post("/plan/{trip_id}/update")
async def update_trip_plan(trip_id: str, request: UpdateRequest) -> dict:
    """Update an existing trip plan with user suggestions.

    Returns the same trip_id. Connect to the stream endpoint to see progress.
    """
    if trip_id not in trip_inputs:
        raise HTTPException(status_code=404, detail="Trip not found. Cannot update.")

    original_inputs = trip_inputs[trip_id]

    # Create updater service and start updating
    service = PlanUpdaterService(trip_id)
    active_sessions[trip_id] = service
    service.start_updating(original_inputs, request.suggestions)

    return {"trip_id": trip_id, "status": "updating"}
