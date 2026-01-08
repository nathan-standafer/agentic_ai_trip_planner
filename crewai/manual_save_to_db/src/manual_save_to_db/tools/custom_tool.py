from crewai.tools import BaseTool
from typing import Type, List, Optional, Union
from pydantic import BaseModel, Field
from .entities import Activity
from .db import save_activity, retrieve_activities
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
    argument: Union[Activity, dict] = Field(..., description="A vacation activity to be processed by the tool. Can be an Activity object or a dictionary.")


class SaveActivityTool(BaseTool):
    name: str = "Save an Activity to the Database"
    description: str = (
        "A tool to save a vacation activity to the database with all its details."
    )
    args_schema: Type[BaseModel] = ActivityInput

    def _run(self, argument: Union[Activity, dict]) -> str:
        """Save the provided `Activity` to the database and return a status message."""
        try:
            # Convert dict to Activity if needed
            if isinstance(argument, dict):
                activity = Activity(**argument)
            else:
                activity = argument
            
            rowid = save_activity(activity)
            return f"Saved Activity with row id {rowid}."
        except Exception as e:
            return f"Failed to save Activity: {e}"


class RetrieveActivitiesInput(BaseModel):
    """Input schema for the RetrieveActivitiesTool."""
    argument: Optional[dict] = Field(default=None, description="Optional argument (not used by this tool).")


class RetrieveActivitiesTool(BaseTool):
    name: str = "Retrieve Activities from the Database"
    description: str = (
        "Retrieve all activities from the database and return them as a list of `Activity` objects."
    )
    args_schema: Type[BaseModel] = RetrieveActivitiesInput

    def _run(self, argument: Optional[dict] = None) -> Union[List[Activity], str]:
        """Return all activities from the DB as a list of `Activity` objects."""
        try:
            activities = retrieve_activities()
            return activities
        except Exception as e:
            return f"Failed to retrieve activities: {e}"

