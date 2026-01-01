# CrewAI Agentic AI Projects

This directory contains projects that demonstrate multi-agent AI systems using [CrewAI](https://crewai.com), a powerful framework for orchestrating AI agents that collaborate on complex tasks.

## What is CrewAI?

CrewAI allows you to create "crews" of AI agents that work together, each with specific roles, goals, and tools. Agents can collaborate sequentially or hierarchically to accomplish tasks that would be difficult for a single agent to complete.

## Prerequisites

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) package manager (recommended)
- An OpenAI API key OR a local LLM setup (like Ollama)

## Project Overview

This directory contains two progressive projects that teach you how to build AI-powered trip planning systems:

1. **basic_trip_planner_crew**: A simple multi-agent system to understand CrewAI fundamentals
2. **trip_planner_with_tools_and_context**: An enhanced version with web search capabilities and contextual knowledge

---

## Project 1: Basic Trip Planner Crew

**Location**: `basic_trip_planner_crew/`

### What You'll Learn

- How to set up a CrewAI project from scratch
- Configuring agents with specific roles and goals
- Defining tasks using YAML configuration
- Running a sequential multi-agent workflow
- Using local LLMs (Ollama) instead of commercial APIs

### Project Structure

The project uses two specialized agents:
- **Researcher**: Finds activities and sightseeing opportunities for a destination
- **Reporting Analyst**: Creates a detailed day-by-day itinerary based on research

### Getting Started

#### 1. Install CrewAI

```bash
# Using UV (recommended)
uv tool install crewai

# OR using pip
pip install crewai
```

#### 2. Navigate to the project directory

```bash
cd crewai/basic_trip_planner_crew
```

#### 3. Install dependencies

```bash
crewai install
```

This command uses UV behind the scenes to manage dependencies. Note: If you have a UV environment activated for other projects, it may conflict. Let CrewAI manage the environment automatically.

#### 4. Configure your LLM

The project is configured to use Ollama with a local LLM model. See [crew.py](basic_trip_planner_crew/src/basic_trip_planner_crew/crew.py#L25-L28) where the LLM is configured:

```python
llm = LLM(
    model="ollama/gpt-oss_131k_context:20b",
    base_url="http://localhost:11434"
)
```

**To use OpenAI instead**:
1. Add your API key to the `.env` file: `OPENAI_API_KEY=sk-...`
2. Modify the LLM configuration in [crew.py](basic_trip_planner_crew/src/basic_trip_planner_crew/crew.py):
   ```python
   llm = LLM(model="openai/gpt-4o-mini")
   ```

**Other LLM options**:
```python
llm = LLM(model="gemini-2-0-flash")  # Google Gemini
llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")  # Llama
```

#### 5. Customize the trip destination

Edit [main.py](basic_trip_planner_crew/src/basic_trip_planner_crew/main.py#L20-L22) to specify your destination:

```python
inputs = {
    'location': 'Tokyo, Japan'  # Change to any destination
}
```

#### 6. Run the crew

```bash
crewai run
```

The crew will:
1. Research activities for your destination
2. Create a detailed day-by-day itinerary
3. Save the output to `report.md`

### Key Configuration Files

- **[agents.yaml](basic_trip_planner_crew/src/basic_trip_planner_crew/config/agents.yaml)**: Defines agent roles, goals, and backstories
- **[tasks.yaml](basic_trip_planner_crew/src/basic_trip_planner_crew/config/tasks.yaml)**: Specifies what each agent should do
- **[crew.py](basic_trip_planner_crew/src/basic_trip_planner_crew/crew.py)**: Orchestrates agents and tasks
- **[main.py](basic_trip_planner_crew/src/basic_trip_planner_crew/main.py)**: Entry point with input parameters

### Understanding the Workflow

1. **Research Task**: The researcher agent searches for interesting activities at the destination
2. **Reporting Task**: The reporting analyst takes the research and creates a structured itinerary

The agents work **sequentially** - the reporting analyst waits for the researcher to finish before starting.

---

## Project 2: Trip Planner with Tools and Context

**Location**: `trip_planner_with_tools_and_context/`

### What You'll Learn

- Adding tools to agents (web search with SerperDev)
- Using task context to pass information between agents
- Incorporating knowledge from files (user preferences)
- Working with dates and structured inputs
- Saving outputs to custom locations

### New Features

Compared to the basic planner, this project adds:
- **Web Search Tool**: Uses SerperDev API for real-time web searches
- **Task Context**: Explicit context passing between tasks for better information flow
- **Date-Aware Planning**: Creates itineraries based on arrival and departure dates
- **User Preferences**: Reads from a knowledge file ([user_preference.txt](trip_planner_with_tools_and_context/knowledge/user_preference.txt)) to personalize the trip

### Getting Started

#### 1. Navigate to the project directory

```bash
cd crewai/trip_planner_with_tools_and_context
```

#### 2. Install dependencies

```bash
crewai install
```

#### 3. Configure API keys

You'll need two API keys for this project:

**Option 1: Using OpenAI + SerperDev (Recommended for beginners)**
1. Get a [SerperDev API key](https://serper.dev/) (free tier available)
2. Create a `.env` file:
   ```
   OPENAI_API_KEY=sk-proj-...
   SERPER_API_KEY=your-serper-key
   ```
3. Update [crew.py](trip_planner_with_tools_and_context/src/trip_planner_with_tools_and_context/crew.py#L31) to use OpenAI:
   ```python
   llm = LLM(model="openai/gpt-4o-mini")
   ```

**Option 2: Using Ollama + SerperDev (Free LLM)**
1. Get a [SerperDev API key](https://serper.dev/)
2. Create a `.env` file:
   ```
   SERPER_API_KEY=your-serper-key
   ```
3. Ensure Ollama is running with your preferred model

#### 4. Customize your trip

Edit [main.py](trip_planner_with_tools_and_context/src/trip_planner_with_tools_and_context/main.py#L19-L23):

```python
inputs = {
    'location': 'Tokyo, Kyoto, and Osaka',
    'arrival_date': '2026-02-26',
    'departure_date': '2026-03-07'
}
```

Edit [knowledge/user_preference.txt](trip_planner_with_tools_and_context/knowledge/user_preference.txt) with your specific requirements:
```
The user's name is Nathan
The family is located in Columbus, OH.
One family member will be running the Tokyo Marathon on March 1, 2026.
The family wants to take the train from Tokyo to visit Kyoto and Osaka on March 3...
```

#### 5. Run the crew

```bash
crewai run
```

The output will be saved to `report.md` with a personalized itinerary that:
- Respects your arrival and departure dates
- Includes calendar dates and days of the week
- Incorporates your specific preferences from the knowledge file
- Uses real-time web search for up-to-date information

### Key Improvements Over Basic Planner

**1. Web Search Tool** ([crew.py](trip_planner_with_tools_and_context/src/trip_planner_with_tools_and_context/crew.py#L34-L39))
```python
@tool('search_tool')
def search_tool(search_query: str):
    """Search the web for information on a given topic"""
    response = SerperDevTool().run(search_query=search_query)
    return response
```
The researcher agent can now search the web for real-time information about activities, events, and attractions.

**2. Task Context** ([tasks.yaml](trip_planner_with_tools_and_context/src/trip_planner_with_tools_and_context/config/tasks.yaml#L16-L18))
```yaml
reporting_task:
  context:
    - research_activities_task
```
The reporting task explicitly receives the output from the research task, ensuring clean information flow.

**3. Date-Aware Planning** ([tasks.yaml](trip_planner_with_tools_and_context/src/trip_planner_with_tools_and_context/config/tasks.yaml#L3-L5))
```yaml
description: >
  Conduct research about activities between {arrival_date} and {departure_date}.
```
The agents know your exact travel dates and plan accordingly.

**4. Knowledge Integration**

The `knowledge/` folder contains context files that agents can reference. This is perfect for:
- User preferences
- Existing bookings (flights, hotels)
- Special requirements (dietary restrictions, accessibility needs)
- Group composition (family with kids, solo travel, etc.)

---

## Creating Your Own CrewAI Project

Want to start from scratch? Here's how to create a new CrewAI project:

```bash
crewai create crew my_project_name
```

You'll be prompted to:
1. Choose an LLM provider (OpenAI, Anthropic, Ollama, etc.)
2. Select a model
3. Enter your API key (if using a commercial provider)

CrewAI will generate a complete project structure with:
- Configuration files for agents and tasks
- A basic crew setup
- Example tools
- A knowledge folder for context

---

## Understanding the CrewAI Architecture

### Agents ([agents.yaml](basic_trip_planner_crew/src/basic_trip_planner_crew/config/agents.yaml))

Agents are defined with:
- **Role**: What the agent is (e.g., "Senior Researcher")
- **Goal**: What the agent should accomplish
- **Backstory**: Context that shapes the agent's behavior
- **Tools** (optional): Functions the agent can use
- **LLM**: The language model powering the agent

### Tasks ([tasks.yaml](basic_trip_planner_crew/src/basic_trip_planner_crew/config/tasks.yaml))

Tasks specify:
- **Description**: What needs to be done
- **Expected Output**: Format and content requirements
- **Agent**: Which agent is responsible
- **Context** (optional): Dependencies on other tasks
- **Output File** (optional): Where to save results

### Crew ([crew.py](basic_trip_planner_crew/src/basic_trip_planner_crew/crew.py#L66-L75))

The crew orchestrates everything:
- **Process**: Sequential or hierarchical execution
- **Agents**: List of participating agents
- **Tasks**: List of tasks to complete
- **Verbose**: Enable detailed logging

---

## Tips and Best Practices

### 1. Start Simple

The basic_trip_planner_crew is intentionally minimal. Master it before moving to the advanced project.

### 2. Use Ollama for Development

Running local LLMs with Ollama is free and fast for development. You can switch to commercial APIs for production.

### 3. Leverage Knowledge Files

Put static context (user preferences, constraints) in the `knowledge/` folder rather than hardcoding it in prompts.

### 4. Test Agent Configurations

Try different:
- Role descriptions
- Goal phrasing
- Backstories

Small changes can significantly impact agent behavior.

### 5. Monitor Agent Interactions

Run with `verbose=True` to see how agents communicate and make decisions. This helps debug issues and optimize workflows.

### 6. Task Dependencies

Use task context to ensure agents have all necessary information:
```yaml
reporting_task:
  context:
    - research_task
```

### 7. Output Formatting

Specify output format clearly in the expected_output field:
```yaml
expected_output: >
  A detailed trip plan formatted as markdown without '```'
```

---

## Common Issues and Solutions

### Issue: UV environment conflicts
**Solution**: Don't manually activate UV environments. Let CrewAI manage them automatically.

### Issue: API rate limits
**Solution**: Use Ollama for unlimited local inference, or upgrade your API plan.

### Issue: Agents not collaborating well
**Solution**: Make sure task context is properly configured and agent goals are specific.

### Issue: Output not formatted correctly
**Solution**: Be explicit in the expected_output field about format requirements.

---

## Next Steps

After completing these projects, consider:

1. **Add more agents**: Create specialized agents (budget tracker, restaurant finder, etc.)
2. **Implement hierarchical process**: Let a manager agent coordinate other agents
3. **Add more tools**: Integrate APIs for weather, flights, hotels, etc.
4. **Use memory**: Enable agents to remember past interactions
5. **Create custom tools**: Build specialized functions for your use case
6. **Experiment with different LLMs**: Compare performance across models

---

## Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Discord Community](https://discord.com/invite/X4JWnZnxPb)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.ai/) - Local LLM hosting
- [SerperDev](https://serper.dev/) - Web search API

---

## Project Comparison

| Feature | Basic Trip Planner | With Tools & Context |
|---------|-------------------|---------------------|
| Web Search | ❌ | ✅ |
| Date-Aware | ❌ | ✅ |
| Task Context | Implicit | Explicit |
| Knowledge Files | ✅ (unused) | ✅ (active) |
| Complexity | Beginner | Intermediate |
| API Requirements | LLM only | LLM + SerperDev |

---

## Contributing

Feel free to:
- Add new agents or tasks
- Experiment with different LLMs
- Create additional example projects
- Share your results and improvements

The goal is to help others understand agentic AI through practical, working examples!
