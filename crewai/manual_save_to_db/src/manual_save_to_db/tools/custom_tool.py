from crewai.tools import BaseTool
from typing import Type, List, Optional, Union
from pydantic import BaseModel, Field
from .entities import Activity, ScheduledActivity
from .db import (
    save_activity, retrieve_activities, save_scheduled_activity, retrieve_schedule,
    activity_exists, delete_scheduled_activity, delete_scheduled_activity_by_name,
    update_scheduled_activity
)
from crewai_tools import SerperDevTool

class SerperToolInput(BaseModel):
    """Input schema for using the SerperTool to perform web searches."""
    search_query: str = Field(..., description="The topic or question to search for online.")

class SerperTool(BaseTool):
    # Use a concise action identifier (avoid long phrases/spaces).
    # Make this match what the agent/LLM is instructed to call.
    name: str = "SerperTool"
    description: str = (
        """
        Search the web for information on a given topic.  Returns a stgring representing the raw search results.
        """
    )
    args_schema: Type[BaseModel] = SerperToolInput

    def _run(self, search_query: str) -> str:
        """Perform a web search and return the raw results."""
        print(f"****************************************** Searching the web for: {search_query}")
        response = SerperDevTool().run(search_query=search_query)
        return response

class ActivityInput(BaseModel):
    """Input schema for the SaveActivityTool."""
    name: str = Field(..., description="The name of the activity")
    description: str = Field(..., description="A description of the activity")
    suggested_duration: str = Field(..., description="Suggested duration for the activity")
    location: str = Field(..., description="The location (city) of the activity")
    sublocation: Optional[str] = Field(None, description="Sublocation like neighborhood")
    http_link: Optional[str] = Field(None, description="URL for more information")
    type: Optional[str] = Field(None, description="Type of activity (e.g., Sightseeing, Shopping)")
    estimated_duration: Optional[str] = Field(None, description="Estimated duration")
    cost: Optional[str] = Field(None, description="Estimated cost")
    suitability: Optional[str] = Field(None, description="Who the activity is suitable for")


class SaveActivityTool(BaseTool):
    name: str = "Save an Activity to the Database"
    description: str = (
        "A tool to save a vacation activity to the database. "
        "Automatically checks if the activity already exists for the given location and skips duplicates. "
        "Pass the fields directly: name, description, suggested_duration, location, sublocation, http_link, type, estimated_duration, cost, suitability."
    )
    args_schema: Type[BaseModel] = ActivityInput

    def _run(self, name: str, description: str, suggested_duration: str, location: str,
             sublocation: Optional[str] = None, http_link: Optional[str] = None,
             type: Optional[str] = None, estimated_duration: Optional[str] = None,
             cost: Optional[str] = None, suitability: Optional[str] = None) -> str:
        """Save the provided activity to the database and return a status message."""
        try:
            # Check if activity already exists for this location
            if activity_exists(name, location):
                return f"Activity '{name}' already exists for location '{location}'. Skipped."

            activity = Activity(
                name=name,
                description=description,
                suggested_duration=suggested_duration,
                location=location,
                sublocation=sublocation,
                http_link=http_link,
                type=type,
                estimated_duration=estimated_duration,
                cost=cost,
                suitability=suitability
            )

            rowid = save_activity(activity)
            return f"Saved Activity '{name}' with row id {rowid}."
        except Exception as e:
            return f"Failed to save Activity: {e}"


class RetrieveActivitiesInput(BaseModel):
    """Input schema for the RetrieveActivitiesTool."""
    location: Optional[str] = Field(default=None, description="Optional location to filter activities (e.g., 'Tokyo', 'Paris'). If not provided, returns all activities.")


class RetrieveActivitiesTool(BaseTool):
    name: str = "Retrieve Activities from the Database"
    description: str = (
        "Retrieve activities from the database filtered by location. "
        "Pass a location (e.g., 'Tokyo', 'Paris', 'Rome') to get only activities for that destination. "
        "If no location is provided, returns all activities."
    )
    args_schema: Type[BaseModel] = RetrieveActivitiesInput

    def _run(self, location: Optional[str] = None) -> Union[List[Activity], str]:
        """Return activities from the DB as a list of `Activity` objects, optionally filtered by location."""
        try:
            activities = retrieve_activities(location=location)
            location_msg = f" for '{location}'" if location else ""
            print(f"Retrieved {len(activities)} activities{location_msg} from database")
            return activities
        except Exception as e:
            return f"Failed to retrieve activities: {e}"


class ScheduledActivityInput(BaseModel):
    """Input schema for the SaveScheduledActivityTool."""
    date: str = Field(..., description="The date in YYYY-MM-DD format")
    time_slot: str = Field(..., description="The time slot, e.g., '09:00 AM'")
    activity_name: str = Field(..., description="Name of the activity")
    activity_description: str = Field(..., description="Brief description of the activity")
    location: str = Field(..., description="Location of the activity")
    duration: str = Field(..., description="Expected duration")
    transportation: Optional[str] = Field(None, description="How to get there")
    notes: Optional[str] = Field(None, description="Additional notes")


class SaveScheduledActivityTool(BaseTool):
    name: str = "Save a Scheduled Activity to the Database"
    description: str = (
        "A tool to save a scheduled vacation activity to the database with date, time, and logistics information. "
        "Pass the fields directly: date, time_slot, activity_name, activity_description, location, duration, transportation, notes."
    )
    args_schema: Type[BaseModel] = ScheduledActivityInput

    def _run(self, date: str, time_slot: str, activity_name: str, activity_description: str,
             location: str, duration: str, transportation: Optional[str] = None,
             notes: Optional[str] = None) -> str:
        """Save the provided scheduled activity to the database and return a status message."""
        try:
            scheduled = ScheduledActivity(
                date=date,
                time_slot=time_slot,
                activity_name=activity_name,
                activity_description=activity_description,
                location=location,
                duration=duration,
                transportation=transportation,
                notes=notes
            )

            rowid = save_scheduled_activity(scheduled)
            return f"Saved ScheduledActivity '{scheduled.activity_name}' for {scheduled.date} at {scheduled.time_slot} with row id {rowid}."
        except Exception as e:
            return f"Failed to save ScheduledActivity: {e}"


class RetrieveScheduleInput(BaseModel):
    """Input schema for the RetrieveScheduleTool."""
    argument: Optional[dict] = Field(default=None, description="Optional argument (not used by this tool).")


class RetrieveScheduleTool(BaseTool):
    name: str = "Retrieve Daily Schedule from the Database"
    description: str = (
        "Retrieve all scheduled activities from the database ordered by date and time. "
        "Returns a list of ScheduledActivity objects with date, time_slot, activity details, and logistics."
    )
    args_schema: Type[BaseModel] = RetrieveScheduleInput

    def _run(self, argument: Optional[dict] = None) -> Union[List[ScheduledActivity], str]:
        """Return all scheduled activities from the DB ordered by date and time."""
        try:
            schedule = retrieve_schedule()
            return schedule
        except Exception as e:
            return f"Failed to retrieve schedule: {e}"


class DeleteScheduledActivityInput(BaseModel):
    """Input schema for the DeleteScheduledActivityTool."""
    activity_name: str = Field(..., description="Name or partial name of the activity to delete")
    date: Optional[str] = Field(None, description="The date in YYYY-MM-DD format (optional, for more precise deletion)")
    time_slot: Optional[str] = Field(None, description="The time slot, e.g., '09:00 AM' (optional, for more precise deletion)")


class DeleteScheduledActivityTool(BaseTool):
    name: str = "Delete Scheduled Activity from Database"
    description: str = (
        "Delete a scheduled activity from the daily schedule. "
        "You can delete by activity name alone (will delete all matching activities), "
        "or provide date and time_slot for more precise deletion. "
        "Use this when the user wants to remove an activity from their plan."
    )
    args_schema: Type[BaseModel] = DeleteScheduledActivityInput

    def _run(self, activity_name: str, date: Optional[str] = None, time_slot: Optional[str] = None) -> str:
        """Delete the specified scheduled activity from the database."""
        try:
            if date and time_slot:
                deleted = delete_scheduled_activity(date, time_slot, activity_name)
            else:
                deleted = delete_scheduled_activity_by_name(activity_name)

            if deleted > 0:
                return f"Deleted {deleted} scheduled activity/activities matching '{activity_name}'."
            else:
                return f"No scheduled activities found matching '{activity_name}'."
        except Exception as e:
            return f"Failed to delete scheduled activity: {e}"


class UpdateScheduledActivityInput(BaseModel):
    """Input schema for the UpdateScheduledActivityTool."""
    date: str = Field(..., description="The date of the activity to update (YYYY-MM-DD)")
    time_slot: str = Field(..., description="The time slot of the activity to update, e.g., '09:00 AM'")
    activity_name: str = Field(..., description="Current name of the activity to update")
    new_activity_name: Optional[str] = Field(None, description="New name for the activity")
    new_activity_description: Optional[str] = Field(None, description="New description for the activity")
    new_time_slot: Optional[str] = Field(None, description="New time slot for the activity")
    new_duration: Optional[str] = Field(None, description="New duration for the activity")
    new_transportation: Optional[str] = Field(None, description="New transportation method")
    new_notes: Optional[str] = Field(None, description="New notes for the activity")


class UpdateScheduledActivityTool(BaseTool):
    name: str = "Update Scheduled Activity in Database"
    description: str = (
        "Update an existing scheduled activity in the daily schedule. "
        "Provide the date, time_slot, and activity_name to identify the activity, "
        "then provide the new values for any fields you want to change. "
        "Use this when the user wants to modify details of an existing activity."
    )
    args_schema: Type[BaseModel] = UpdateScheduledActivityInput

    def _run(
        self,
        date: str,
        time_slot: str,
        activity_name: str,
        new_activity_name: Optional[str] = None,
        new_activity_description: Optional[str] = None,
        new_time_slot: Optional[str] = None,
        new_duration: Optional[str] = None,
        new_transportation: Optional[str] = None,
        new_notes: Optional[str] = None
    ) -> str:
        """Update the specified scheduled activity in the database."""
        try:
            updated = update_scheduled_activity(
                date=date,
                time_slot=time_slot,
                activity_name=activity_name,
                new_activity_name=new_activity_name,
                new_activity_description=new_activity_description,
                new_time_slot=new_time_slot,
                new_duration=new_duration,
                new_transportation=new_transportation,
                new_notes=new_notes
            )

            if updated > 0:
                return f"Updated {updated} scheduled activity/activities matching '{activity_name}' on {date} at {time_slot}."
            else:
                return f"No scheduled activities found matching '{activity_name}' on {date} at {time_slot}."
        except Exception as e:
            return f"Failed to update scheduled activity: {e}"

