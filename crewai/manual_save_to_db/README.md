# AI Vacation Planner

An intelligent vacation planning application powered by [CrewAI](https://crewai.com) that uses multiple AI agents to research activities, create daily schedules, and generate comprehensive trip itineraries. Features a modern web interface with real-time progress updates.

## What It Does

The AI Vacation Planner automates the entire trip planning process:

1. **Research Phase**: An AI agent searches the web for activities at your destination, considering weather conditions, travel dates, and your preferences
2. **Data Persistence**: Activities are saved to a SQLite database, enabling reuse across trips to the same location
3. **Schedule Creation**: Another agent creates a day-by-day schedule with appropriate time slots, transportation, and logistics
4. **Report Generation**: A final agent produces a detailed, formatted itinerary with costs, tips, and recommendations
5. **Plan Updates**: After reviewing your plan, you can request specific changes (add/remove/modify activities) and the AI will update accordingly

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Frontend (React + Vite)                        │
│  ┌──────────────┐  ┌───────────────────┐  ┌────────────────────────┐   │
│  │   TripForm   │  │  ProgressDisplay  │  │    ResultsDisplay      │   │
│  │  (user input)│  │  (SSE streaming)  │  │  (itinerary + update)  │   │
│  └──────────────┘  └───────────────────┘  └────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HTTP + SSE
┌────────────────────────────────▼────────────────────────────────────────┐
│                        Backend (FastAPI + Uvicorn)                       │
│  ┌─────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │   /api/trips    │  │  TripPlannerService │  │ PlanUpdaterService │  │
│  │   REST API      │  │  (crew execution)   │  │  (plan updates)    │  │
│  └─────────────────┘  └─────────────────────┘  └────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                         CrewAI Agent Pipeline                            │
│                                                                          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐  │
│  │ Activity        │    │ Activity Saver  │    │ Daily Planner       │  │
│  │ Researcher      │───▶│ Agent           │───▶│ Agent               │  │
│  │ (web search)    │    │ (save to DB)    │    │ (schedule creation) │  │
│  └─────────────────┘    └─────────────────┘    └──────────┬──────────┘  │
│                                                           │              │
│                         ┌─────────────────────────────────▼──────────┐  │
│                         │ Reporting Analyst                          │  │
│                         │ (itinerary generation)                     │  │
│                         └────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                          SQLite Database                                 │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────┐   │
│  │ activities              │  │ daily_schedule                      │   │
│  │ (name, location, type,  │  │ (date, time_slot, activity_name,   │   │
│  │  cost, duration, etc.)  │  │  transportation, notes, etc.)       │   │
│  └─────────────────────────┘  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | React 18, TypeScript, Vite | User interface with form, progress tracking, results display |
| Backend API | FastAPI, Uvicorn | REST endpoints, SSE streaming, session management |
| AI Agents | CrewAI, Claude Haiku 4.5 | Research, scheduling, and report generation |
| Database | SQLite | Persistent storage for activities and schedules |
| Web Search | Serper API | Real-time activity research |

### Agent Roles

1. **Activity Researcher**: Searches for weather-appropriate activities based on destination and travel dates
2. **Activity Saver**: Persists researched activities to the database, detecting duplicates
3. **Daily Planner**: Creates time-slotted schedules for each day of the trip
4. **Reporting Analyst**: Generates formatted markdown itineraries with costs and tips
5. **Plan Updater**: Handles user-requested modifications to existing plans

## Installation

### Prerequisites

- Python 3.10 - 3.13
- Node.js 18+
- [UV](https://docs.astral.sh/uv/) package manager (recommended)

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd manual_save_to_db
   ```

2. **Install Python dependencies:**
   ```bash
   pip install uv
   crewai install
   ```

3. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure environment variables:**

   Create a `.env` file in the project root:
   ```env
   CLAUDE_API_KEY=your_anthropic_api_key
   SERPER_API_KEY=your_serper_api_key
   ```

## Running the Application

### Option 1: Web Interface (Recommended)

Start both the backend and frontend:

**Terminal 1 - Backend:**
```bash
cd /path/to/manual_save_to_db
PYTHONPATH=src uvicorn manual_save_to_db.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd /path/to/manual_save_to_db/frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

### Option 2: Command Line

For CLI-only usage without the web interface:
```bash
crewai run
```

This uses the default trip parameters defined in `src/manual_save_to_db/main.py`.

## Usage

### Planning a Trip

1. Fill out the trip form with:
   - **Destination(s)** - e.g., "Tokyo, Japan" or "Paris and Rome"
   - **Arrival Date** - When your trip starts
   - **Departure Date** - When your trip ends
   - **Desired Activities** - Types of activities you enjoy (optional)
   - **Other Considerations** - Special requirements, accessibility needs, etc. (optional)
   - **Food Preferences** - Dietary restrictions or cuisine preferences (optional)

2. Click "Plan My Vacation" and watch the real-time progress as agents work

3. Review your generated itinerary with:
   - Day-by-day schedule with times and activities
   - Transportation recommendations
   - Cost estimates
   - Trip summary and highlights

### Updating a Plan

After viewing your plan, you can request changes:
- "Add a visit to the Eiffel Tower on day 2"
- "Remove the museum visit on the last day"
- "Replace the afternoon activity on Jan 18th with shopping"

The AI will modify only the specific items you mention.

### Exporting

Click "Export PDF" to download your itinerary for offline use.

## Project Structure

```
manual_save_to_db/
├── src/manual_save_to_db/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py             # App entry point
│   │   ├── routers/trips.py    # API endpoints
│   │   ├── schemas/trip.py     # Pydantic models
│   │   └── services/           # Crew execution services
│   ├── config/
│   │   ├── agents.yaml         # Agent definitions
│   │   └── tasks.yaml          # Task definitions
│   ├── tools/
│   │   ├── custom_tool.py      # CrewAI tools (Serper, DB operations)
│   │   ├── db.py               # SQLite database functions
│   │   └── entities.py         # Pydantic models for activities
│   ├── crew.py                 # Crew and agent configuration
│   └── main.py                 # CLI entry point
├── frontend/
│   └── src/
│       ├── components/         # React components
│       ├── hooks/useSSE.ts     # Server-Sent Events hook
│       ├── services/api.ts     # API client
│       └── styles/index.css    # Styling
├── output/                     # Generated reports
└── VacationPlanner.db          # SQLite database
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/trips/plan` | Start a new trip planning session |
| GET | `/api/trips/plan/{id}/stream` | SSE stream for real-time progress |
| GET | `/api/trips/plan/{id}/result` | Get final itinerary and schedule |
| POST | `/api/trips/plan/{id}/update` | Update existing plan with changes |
| DELETE | `/api/trips/plan/{id}` | Clean up a planning session |
| GET | `/health` | Health check endpoint |

## Configuration

### LLM Settings

The application uses Claude Haiku 4.5 by default. To change models, edit `src/manual_save_to_db/crew.py`:

```python
# For local Ollama models
ollama_llm = LLM(
    model="ollama/gemma3_128k:12b",
    base_url="http://localhost:11434"
)

# For Claude
claude_llm = LLM(
    model="claude-haiku-4-5",
)
```

### Agent Iterations

Adjust `max_iter` in agent definitions if agents need more steps:
- Research agent: 25 iterations (thorough web searches)
- Saver agent: 50 iterations (one per activity)
- Planner agent: 100 iterations (scheduling all days)
- Reporter agent: 15 iterations (report generation)

## Future Enhancements

### Near-Term Improvements

1. **User Accounts & Trip History**
   - Save trips to user profiles
   - View and manage past itineraries
   - Share trips with travel companions

2. **Enhanced Weather Integration**
   - Real-time weather forecasts for travel dates
   - Automatic activity rescheduling for bad weather
   - Indoor/outdoor activity balance optimization

3. **Budget Management**
   - Set trip budget constraints
   - Track estimated vs. actual costs
   - Budget-aware activity recommendations

4. **Multi-Destination Routing**
   - Optimize travel routes between cities
   - Suggest logical ordering of destinations
   - Include inter-city transportation options

### Medium-Term Features

5. **Booking Integration**
   - Direct links to book activities
   - Hotel and flight recommendations
   - Restaurant reservations

6. **Collaborative Planning**
   - Share plans with travel group
   - Vote on activities
   - Merge preferences from multiple users

7. **Mobile App**
   - Native iOS/Android apps
   - Offline access to itineraries
   - Location-based notifications

8. **AI Improvements**
   - Learn from user feedback
   - Personalized recommendations based on past trips
   - Natural language plan modifications

### Long-Term Vision

9. **Real-Time Adaptation**
   - Adjust plans based on current conditions
   - Handle cancellations and closures
   - Alternative activity suggestions

10. **Travel Community**
    - User reviews and ratings
    - Shared itinerary templates
    - Local expert recommendations

## Troubleshooting

### "No schedule data available"
- Ensure the backend is running from the project root directory
- Check that `VacationPlanner.db` exists in the project root
- Verify the database path in logs: `Retrieving schedule from database: /path/to/VacationPlanner.db`

### Agents not making progress
- Check API keys in `.env` file
- Increase `max_iter` for the stuck agent
- Review backend logs for error messages

### SSE connection issues
- Ensure no proxy is buffering responses
- Check that port 8000 is accessible
- Try refreshing the browser

## License

This project is for educational and personal use.

## Acknowledgments

- [CrewAI](https://crewai.com) - Multi-agent AI framework
- [Anthropic Claude](https://anthropic.com) - AI language model
- [Serper](https://serper.dev) - Web search API
- [FastAPI](https://fastapi.tiangolo.com) - Python web framework
- [React](https://react.dev) - Frontend framework
