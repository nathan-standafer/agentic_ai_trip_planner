from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from crewai.tools import tool
from pydantic import BaseModel, Field
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class Activity(BaseModel):
    """A sightseeing or other vacation-related activity with its details."""
    name: str = Field(description="A short name of the activity")
    description: str = Field(description="A description of the activity, about 20 world in length.")
    suggested_duration: str = Field(description="The suggested duration for the activity, e.g., '2 hours', 'half day', 'full day'.")
    location: str = Field(description="The location where the activity takes place, e.g., city or specific venue.")
    sublocation: str = Field(description="The specific sub-location or venue within the main location where the activity takes place.")

class ActivityList(BaseModel):
    """A list of activities with their details."""
    activities: List[Activity] = Field(description="A list of activities with their details.")  

class DailyActivityPlan(BaseModel):
    """A daily plan of activities."""
    date: str = Field(description="The date for the activities, in YYYY-MM-DD format.")
    activities: List[Activity] = Field(description="A list of activities planned for the day.")

class DailyActivityPlanList(BaseModel):
    """A list of daily activity plans."""
    daily_plans: List[DailyActivityPlan] = Field(description="A list of daily activity plans.")


@CrewBase
class ManagerAgent():
    """ManagerAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    llm = LLM(
        model="ollama/gemma3_128k:12b",        
        base_url="http://localhost:11434"
    )

    @tool('search_tool')
    def search_tool(search_query: str):
        """
        Search the web for information on a given topic.

        Usage:
        - Pass a clear and concise search_query string describing what you want to find.
        - The tool will use SerperDevTool to perform a web search and return the results.
        - Use this tool when you need up-to-date information or details not present in local knowledge sources.

        Example:
        search_tool('Best sightseeing spots in Paris')

        Args:
            search_query (str): The topic or question to search for online.
        Returns:
            str: The search results from SerperDevTool.
        """
        print(f"Searching the web for: {search_query}")
        response = SerperDevTool().run(search_query=search_query)
        return response
    
    @agent
    def researcher_activities(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_activities'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool],
            llm=self.llm,
            output_pydantic=ActivityList
        )
    
    @agent
    def coordinator_activities(self) -> Agent:
        return Agent(
            config=self.agents_config['coordinator_activities'], # type: ignore[index]
            verbose=True,
            #tools=[self.search_tool],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )
    
    @agent
    def researcher_food(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_food'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )
    
    @agent
    def researcher_lodging(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_lodging'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )   
    
    @agent
    def researcher_transportation(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_transportation'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True,
            llm=self.llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_activities_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_activities_task'], # type: ignore[index]
        )

    @task
    def coordinator_activities_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordinator_activities_task'], # type: ignore[index]
        )  

    @task
    def research_food_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_food_task'], # type: ignore[index]
        )  
    
    @task
    def research_lodging_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_lodging_task'], # type: ignore[index]
        )  
        
    @task
    def research_transportation_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_transportation_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            #output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StructuredOutputsWithMoreAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
