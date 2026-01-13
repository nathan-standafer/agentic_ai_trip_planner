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
from .tools.custom_tool import SaveActivityTool, RetrieveActivitiesTool, SerperTool, SaveScheduledActivityTool, RetrieveScheduleTool

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
