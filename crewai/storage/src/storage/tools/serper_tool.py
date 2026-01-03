from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool

class SerperToolInput(BaseModel):
    """Input schema for using the Serper Dev tool to perform web searches."""
    search_query: str = Field(..., description="The topic or question to search for online.")

class SerperTool(BaseTool):
    # Use a concise action identifier (avoid long phrases/spaces).
    # Make this match what the agent/LLM is instructed to call.
    name: str = "SerperTool"
    description: str = (
        """
        Search the web for information on a given topic.

        Usage:
        - Pass a clear and concise search_query string describing what you want to find.
        - The tool will use SerperDevTool to perform a web search and return the results.
        - Use this tool when you need up-to-date information or details not present in local knowledge sources.

         Returns:
            str: The search results from SerperDevTool.
        """
    )
    args_schema: Type[BaseModel] = SerperToolInput

    def _run(self, search_query: str) -> str:
        # Implementation goes here
        print(f"Searching the web for: {search_query}")
        response = SerperDevTool().run(search_query=search_query)
        return response
