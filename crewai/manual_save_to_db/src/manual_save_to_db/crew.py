import os
from dotenv import load_dotenv

# Load .env before any other imports
load_dotenv()

# Map CLAUDE_API_KEY to ANTHROPIC_API_KEY if needed
if os.getenv("CLAUDE_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = os.getenv("CLAUDE_API_KEY")

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from datetime import datetime
from .tools.entities import Activity, ScheduledActivity
from .tools.custom_tool import (
    SaveActivityTool, RetrieveActivitiesTool, SerperTool,
    SaveScheduledActivityTool, RetrieveScheduleTool,
    DeleteScheduledActivityTool, UpdateScheduledActivityTool
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ManualSaveToDb():
    """ManualSaveToDb crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Local Ollama LLM - available for agents that don't need Claude
    ollama_llm = LLM(
        model="ollama/gemma3_128k:12b",       #GOOD the best local LLM so far
        base_url="http://localhost:11434"
    )

    # Claude Haiku 4.5 - uses CLAUDE_API_KEY from .env (mapped to ANTHROPIC_API_KEY above)
    claude_llm = LLM(
        model="claude-haiku-4-5",
    )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def activity_researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['activity_researcher_agent'], # type: ignore[index]
            verbose=True,
            tools=[SerperTool(), RetrieveActivitiesTool()],
            llm=self.claude_llm,
            max_iter=25,  # Allow enough iterations for thorough research
        )

    @agent
    def activity_saver_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['activity_saver_agent'], # type: ignore[index]
            verbose=True,
            tools=[SaveActivityTool()],
            llm=self.claude_llm,
            max_iter=50,  # Must be high enough to save all activities (one tool call per activity)
        )

    @agent
    def daily_planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['daily_planner_agent'], # type: ignore[index]
            verbose=True,
            tools=[RetrieveActivitiesTool(), SaveScheduledActivityTool(), RetrieveScheduleTool()],  # Added RetrieveScheduleTool
            llm=self.claude_llm,
            max_iter=100,  # Must be high enough to save all activities (one tool call per activity)
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True,
            tools=[RetrieveScheduleTool()],
            llm=self.claude_llm,
            max_iter=15,  # Default is fine for reporting
        )

    # Defined entirely in code - not in YAML to avoid CrewBase auto-mapping issues
    def plan_updater_agent(self, location: str) -> Agent:
        return Agent(
            role=f"Vacation Plan Updater for trips to {location}",
            goal="Update the existing vacation plan based ONLY on the user's specific suggestions. Do NOT make any changes beyond what the user explicitly requested.",
            backstory="""You are a precise and careful plan editor. When users request changes to their
vacation plans, you make EXACTLY the changes they ask for - no more, no less.
If a user asks to add an activity, you add only that activity.
If a user asks to remove something, you remove only that item.
If a user asks to modify details, you change only those specific details.
You NEVER make assumptions about what else the user might want changed.
You use the appropriate tools: DeleteScheduledActivityTool to remove activities,
UpdateScheduledActivityTool to modify existing activities, and
SaveScheduledActivityTool to add new activities.""",
            verbose=True,
            tools=[
                RetrieveScheduleTool(),
                SaveScheduledActivityTool(),
                DeleteScheduledActivityTool(),
                UpdateScheduledActivityTool(),
                RetrieveActivitiesTool(),
                SerperTool(),  # In case user wants to add a new activity that needs research
            ],
            llm=self.claude_llm,
            max_iter=30,  # Enough for multiple updates
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def activity_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['activity_research_task'], # type: ignore[index]
            output_file=f'output/activities_{datetime.now().strftime("%Y%m%d-%H%M")}.md'
        )
    
    @task
    def save_activities_task(self) -> Task:
        return Task(
            config=self.tasks_config['save_activities_task'], # type: ignore[index]
        )

    @task
    def scheduling_task(self) -> Task:
        return Task(
            config=self.tasks_config['scheduling_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file=f'output/report_{datetime.now().strftime("%Y%m%d-%H%M")}.md'
        )

    # Defined entirely in code - not in YAML to avoid CrewBase auto-mapping issues
    def update_plan_task(self, location: str, arrival_date: str, user_suggestions: str, agent: Agent) -> Task:
        return Task(
            description=f"""Update the vacation plan for {location} based on the user's specific suggestions.

USER'S REQUESTED CHANGES:
{user_suggestions}

STEP-BY-STEP INSTRUCTIONS (you MUST follow these steps and use the tools):

STEP 1: Call "Retrieve Daily Schedule from the Database" to see current activities.

STEP 2: Analyze the user's request and determine what needs to change.

STEP 3: Execute the required changes using the appropriate tool(s):
   - To ADD a new activity: Call "Save a Scheduled Activity to the Database" with all required fields
   - To REMOVE an activity: Call "Delete Scheduled Activity from Database" with the activity name
   - To REPLACE an activity: First DELETE the old one, then ADD the new one
   - To MODIFY an activity: Call "Update Scheduled Activity in Database"

STEP 4: Call "Retrieve Daily Schedule from the Database" again to verify changes were made.

STEP 5: Generate the updated trip report showing all scheduled activities.

IMPORTANT:
- The arrival date is {arrival_date}. If user says "day 2", that means the day after {arrival_date}.
- You MUST actually call the tools - do not just describe what you would do.
- Make ONLY the changes requested - nothing more.""",
            expected_output="""A confirmation of the changes made, followed by the updated trip itinerary report.

Format:
## Changes Made
- [List each specific change you made based on user request]

## Updated Trip Itinerary
[Full updated itinerary in the same format as the original report]""",
            agent=agent,
            output_file=f'output/updated_report_{datetime.now().strftime("%Y%m%d-%H%M")}.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ManualSaveToDb crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    def update_crew(self, location: str, arrival_date: str, user_suggestions: str) -> Crew:
        """Creates a crew specifically for updating an existing plan."""
        agent = self.plan_updater_agent(location)
        task = self.update_plan_task(location, arrival_date, user_suggestions, agent)
        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
