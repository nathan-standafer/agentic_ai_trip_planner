from pydantic import BaseModel, Field
from typing import Optional


class Activity(BaseModel):
    """A sightseeing or other vacation-related activity with its details."""
    name: str = Field(description="A short name of the activity")
    description: str = Field(description="A description of the activity, about 20 world in length.")
    suggested_duration: str = Field(description="The suggested duration for the activity, e.g., '2 hours', 'half day', 'full day'.")
    location: str = Field(description="The location where the activity takes place, e.g., city or specific venue.")
    sublocation: str = Field(description="The specific sub-location or venue within the main location where the activity takes place.")
    http_link: str = Field(description="A URL link to more information about the activity, if available.")
    
    # Additional optional fields that agents may provide
    type: Optional[str] = Field(None, description="The type of activity, e.g., 'Sightseeing', 'Dining', 'Adventure'.")
    estimated_duration: Optional[str] = Field(None, description="Estimated duration for the activity.")
    cost: Optional[str] = Field(None, description="Estimated cost of the activity.")
    suitability: Optional[str] = Field(None, description="Who the activity is suitable for, e.g., 'All ages', 'Adults only'.")


class ScheduledActivity(BaseModel):
    """A scheduled activity with date, time, and logistics information."""
    date: str = Field(description="The date for this activity in YYYY-MM-DD format.")
    time_slot: str = Field(description="The start time for the activity, e.g., '09:00 AM'.")
    activity_name: str = Field(description="The name of the activity.")
    activity_description: str = Field(description="A brief description of the activity.")
    location: str = Field(description="The location where the activity takes place.")
    duration: str = Field(description="Expected duration of the activity, e.g., '2 hours'.")
    transportation: Optional[str] = Field(None, description="How to get to the activity location, including travel time.")
    notes: Optional[str] = Field(None, description="Additional notes such as weather tips, reservations needed, or seasonal info.")