"""Pydantic schemas for trip planning API."""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import date
from enum import Enum


class TripStatus(str, Enum):
    """Status of a trip planning session."""
    PENDING = "pending"
    RESEARCHING = "researching_activities"
    SAVING = "saving_activities"
    SCHEDULING = "scheduling_activities"
    REPORTING = "generating_report"
    COMPLETED = "completed"
    ERROR = "error"


class TripRequest(BaseModel):
    """Request schema for starting trip planning."""
    arrival_date: date = Field(..., description="Trip arrival date (YYYY-MM-DD)")
    departure_date: Optional[date] = Field(None, description="Trip departure date")
    destinations: str = Field(..., min_length=1, description="Comma-separated list of destinations")
    desired_activities: Optional[str] = Field(None, description="Semicolon-separated desired activities")
    other_considerations: Optional[str] = Field(None, description="Semicolon-separated trip considerations")
    food_considerations: Optional[str] = Field(None, description="Semicolon-separated food preferences")

    @field_validator('arrival_date')
    @classmethod
    def validate_arrival_not_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Arrival date cannot be in the past")
        return v

    @model_validator(mode='after')
    def validate_dates(self) -> 'TripRequest':
        if self.departure_date and self.arrival_date:
            if self.departure_date <= self.arrival_date:
                raise ValueError("Departure date must be after arrival date")
        return self


class UpdateRequest(BaseModel):
    """Request schema for updating an existing trip plan."""
    suggestions: str = Field(..., min_length=1, description="User suggestions for updating the plan")


class ProgressEvent(BaseModel):
    """SSE progress event structure."""
    event_type: str  # "start", "task_start", "task_complete", "step", "complete", "error"
    task_name: Optional[str] = None
    agent_name: Optional[str] = None
    message: str
    progress_percent: int  # 0-100, -1 for indeterminate
    timestamp: str
    trip_id: str


class ScheduledActivityResponse(BaseModel):
    """Response schema for a scheduled activity."""
    date: str
    time_slot: str
    activity_name: str
    activity_description: str
    location: str
    duration: str
    transportation: Optional[str] = None
    notes: Optional[str] = None


class TripResponse(BaseModel):
    """Response after trip planning completes."""
    trip_id: str
    status: TripStatus
    result: Optional[str] = None
    schedule: Optional[List[ScheduledActivityResponse]] = None
    error_message: Optional[str] = None
