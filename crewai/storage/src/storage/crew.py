from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# from crewai_tools import SerperDevTool
# from crewai.tools import tool
from pydantic import BaseModel, Field
from .tools.serper_tool import SerperTool
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
    http_link: str = Field(description="A URL link to more information about the activity, if available.")

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
    #gemma3 seems to work the best for this project.  I experimmented with other local LLMs and openai models, but they would never perform as well as gemma3.
    llm = LLM(
        #model="openai/gpt-4o-mini",

        model="ollama/gemma3_128k:12b",       #GOOD the best local LLM so far
        #model="ollama/granite4:3b",   #failed to call the SerperDev tool and lost its say.  But, it really followed the general instructions.  I might needd to increase the context length
        #model="ollama/granite4_128k:3b",  #it was able to call the SerperDev tool, but the final report was not very good.
        #model="ollama/deepseek-r1:14b",  #this worked pretty well, but was slower.  
        #model="ollama/deepseek-r1_32k:14b", #GOOD this did well, but got the days of the week wrong.
        base_url="http://localhost:11434"

        #model='gemini/gemini-3-pro-preview',  #it immediately tells me I need to pay up
        #model='gemini/gemini-3-flash-preview', #this works well, but I ran out of free credits quickly.  Having trought setting up a key with billing.  

        #model="groq/qwen/qwen3-32b"  #this one seems to work well with tool calling, but didn't produce a good final report
        #model="groq/moonshotai/kimi-k2-instruct-0905" #fails. Produces an error: Received None or empty response from LLM call.  An unknown error occurred. Please check the details below.
        #model="groq/openai/gpt-oss-120b"  #fails as well with same error as above.
        #model="groq/llama-3.3-70b-versatile"  #tool calling works well.  produces a final report, although the durations are a little wonky.
        #model="groq/meta-llama/llama-4-maverick-17b-128e-instruct" # same errors as kimi and oss

    )
    
    @agent
    def researcher_activities(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_activities'],
            verbose=True,
            tools=[SerperTool()],
            llm=self.llm,
            #output_pydantic=ActivityList
            output_json=ActivityList,
            output_file='output/activities_list_json.json'
        )
    
    @agent
    def coordinator_activities(self) -> Agent:
        return Agent(
            config=self.agents_config['coordinator_activities'],
            verbose=True,
            #tools=[SerperTool()],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )
    
    @agent
    def researcher_food(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_food'],
            verbose=True,
            tools=[SerperTool()],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )
    
    @agent
    def researcher_lodging(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_lodging'],
            verbose=True,
            tools=[SerperTool()],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )   
    
    @agent
    def researcher_transportation(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_transportation'],
            verbose=True,
            tools=[SerperTool()],
            llm=self.llm,
            output_pydantic=DailyActivityPlanList
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            llm=self.llm,
            markdown=True
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
        """Creates the ManagerAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # manager = Agent(
        #     config=self.agents_config['manager'], # type: ignore[index]
        #     verbose=True,
        #     allow_delegation=True,
        #     llm=self.llm
        # )

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True
            #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            #manager_agent=manager
        )
