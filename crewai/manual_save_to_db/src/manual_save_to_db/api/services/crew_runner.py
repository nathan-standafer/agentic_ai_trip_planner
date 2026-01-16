"""Service for running CrewAI crews with real-time progress tracking."""

import asyncio
import json
import traceback
import sys
from datetime import datetime
from typing import AsyncGenerator, Dict, Any, Optional
from queue import Queue
import threading

from crewai import TaskOutput


class TripPlannerService:
    """Service for running CrewAI crews with real-time progress tracking via SSE."""

    # Map task names to human-readable descriptions and progress percentages
    TASK_PROGRESS_MAP = {
        "activity_research": ("Researching activities", 25),
        "save_activities": ("Saving activities to database", 50),
        "scheduling": ("Creating daily schedule", 75),
        "reporting": ("Generating final report", 95),
    }

    def __init__(self, trip_id: str):
        self.trip_id = trip_id
        self.event_queue: Queue = Queue()
        self.is_running = False
        self.error: Optional[str] = None
        self.result: Optional[str] = None

    def _create_progress_event(
        self,
        event_type: str,
        message: str,
        progress: int,
        task_name: Optional[str] = None,
        agent_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a standardized progress event."""
        return {
            "event_type": event_type,
            "task_name": task_name,
            "agent_name": agent_name,
            "message": message,
            "progress_percent": progress,
            "timestamp": datetime.now().isoformat(),
            "trip_id": self.trip_id
        }

    def _task_callback(self, output: TaskOutput) -> None:
        """Callback executed after each task completes."""
        task_name = output.name or (output.description[:50] if output.description else "Unknown task")
        agent = output.agent if hasattr(output, 'agent') else None

        # Determine progress based on task name
        progress = 25  # default
        human_name = task_name
        for key, (name, pct) in self.TASK_PROGRESS_MAP.items():
            if key in task_name.lower():
                human_name = name
                progress = pct
                break

        event = self._create_progress_event(
            event_type="task_complete",
            message=f"Completed: {human_name}",
            progress=progress,
            task_name=human_name,
            agent_name=agent
        )
        self.event_queue.put(event)

    def _step_callback(self, step_output: Any) -> None:
        """Callback executed after each agent step."""
        # Extract meaningful info from step output
        message = "Agent working..."
        if step_output:
            step_str = str(step_output)
            # Truncate long messages
            if len(step_str) > 150:
                step_str = step_str[:150] + "..."
            message = step_str

        event = self._create_progress_event(
            event_type="step",
            message=message,
            progress=-1  # -1 indicates indeterminate progress
        )
        self.event_queue.put(event)

    def _run_crew_sync(self, inputs: Dict[str, Any]) -> None:
        """Run the crew synchronously in a thread."""
        try:
            self.is_running = True

            # Import here to avoid circular imports and ensure env is loaded
            from manual_save_to_db.crew import ManualSaveToDb
            from manual_save_to_db.tools.db import retrieve_schedule, clear_schedule

            # Clear previous schedule data before starting new plan
            deleted_count = clear_schedule()
            print(f"Cleared {deleted_count} previous schedule entries", file=sys.stderr)

            # Send start event
            self.event_queue.put(self._create_progress_event(
                event_type="start",
                message="Starting vacation planning...",
                progress=0
            ))

            # Create crew instance
            crew_instance = ManualSaveToDb()
            crew = crew_instance.crew()

            # Inject callbacks
            crew.task_callback = self._task_callback
            crew.step_callback = self._step_callback

            # Execute crew
            result = crew.kickoff(inputs=inputs)

            # Store result
            self.result = str(result) if result else "Planning complete"

            # Send completion event
            self.event_queue.put(self._create_progress_event(
                event_type="complete",
                message="Vacation plan complete!",
                progress=100
            ))

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            print(f"CrewAI Error: {error_msg}", file=sys.stderr)
            print(f"Traceback:\n{tb}", file=sys.stderr)
            self.error = error_msg
            self.event_queue.put(self._create_progress_event(
                event_type="error",
                message=f"Error: {error_msg}",
                progress=-1
            ))
        finally:
            self.is_running = False
            self.event_queue.put(None)  # Sentinel to stop SSE stream

    def start_planning(self, inputs: Dict[str, Any]) -> None:
        """Start crew execution in background thread."""
        thread = threading.Thread(
            target=self._run_crew_sync,
            args=(inputs,),
            daemon=True
        )
        thread.start()

    async def stream_progress(self) -> AsyncGenerator[str, None]:
        """Async generator for SSE progress events."""
        print("SSE stream_progress started", file=sys.stderr)
        while True:
            # Check queue in non-blocking way
            await asyncio.sleep(0.1)

            try:
                # Non-blocking get from queue
                if not self.event_queue.empty():
                    event = self.event_queue.get_nowait()

                    if event is None:  # Sentinel
                        print("SSE stream_progress: received sentinel, stopping", file=sys.stderr)
                        return

                    # Format and yield the event data
                    event_json = json.dumps(event)
                    print(f"SSE yielding event: {event['event_type']}", file=sys.stderr)
                    yield event_json
            except Exception as e:
                print(f"SSE stream error: {e}", file=sys.stderr)
