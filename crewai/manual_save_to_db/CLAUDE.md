# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrewAI-based vacation trip planner that uses multiple AI agents to research activities, save them to a SQLite database, and generate detailed trip itineraries. The project demonstrates manual database persistence with CrewAI agents.

## Commands

```bash
# Install dependencies (uses UV package manager)
crewai install

# Run the crew (main execution)
crewai run

# Train the crew
python -m manual_save_to_db.main train <iterations> <filename>

# Replay from a specific task
python -m manual_save_to_db.main replay <task_id>

# Database CLI commands
PYTHONPATH=src python -m manual_save_to_db.tools.db init          # Initialize database
PYTHONPATH=src python -m manual_save_to_db.tools.db show-tables   # List tables
PYTHONPATH=src python -m manual_save_to_db.tools.db save-sample   # Insert sample activity
```

## Architecture

### Agent Pipeline (Sequential Process)
1. **activity_researcher_agent** - Searches web using SerperTool, finds vacation activities
2. **activity_saver_agent** - Persists activities to SQLite using SaveActivityTool
3. **daily_planner_agent** - Reads activities from DB, schedules them with dates/times using SerperTool for logistics, saves to daily_schedule table
4. **reporting_analyst** - Retrieves daily schedule from DB, generates formatted itinerary

### Key Files
- `src/manual_save_to_db/crew.py` - Crew definition with agents, tasks, and LLM config
- `src/manual_save_to_db/main.py` - Entry points and trip input configuration
- `src/manual_save_to_db/tools/custom_tool.py` - Custom CrewAI tools (SerperTool, SaveActivityTool, RetrieveActivitiesTool, SaveScheduledActivityTool, RetrieveScheduleTool)
- `src/manual_save_to_db/tools/db.py` - SQLite database operations
- `src/manual_save_to_db/tools/entities.py` - Pydantic models (Activity, ScheduledActivity)
- `config/agents.yaml` - Agent role/goal/backstory definitions
- `config/tasks.yaml` - Task descriptions and expected outputs

### Database
- SQLite database: `VacationPlanner.db` (created in working directory)
- Tables:
  - `activities` - Raw vacation activities with name, description, location, etc.
  - `daily_schedule` - Scheduled activities with date, time_slot, transportation, notes

### LLM Configuration
The crew uses a local Ollama model by default:
```python
LLM(model="ollama/gemma3_128k:12b", base_url="http://localhost:11434")
```

### Environment Variables
- `SERPER_API_KEY` - Required for web search functionality (SerperDevTool)
- `OPENAI_API_KEY` - If switching to OpenAI models

### Output Files
- `output/activities.md` - Raw activity research results
- `output/report.md` - Final formatted trip itinerary
