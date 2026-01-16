"""FastAPI application for the vacation planner web interface."""

import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Load environment variables from the project root
project_root = Path(__file__).parent.parent.parent.parent.parent
load_dotenv(project_root / ".env")

# Map CLAUDE_API_KEY to ANTHROPIC_API_KEY if needed
if os.getenv("CLAUDE_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = os.getenv("CLAUDE_API_KEY")

from .routers import trips

app = FastAPI(
    title="Vacation Planner API",
    description="AI-powered vacation planning with CrewAI agents",
    version="1.0.0"
)

# CORS configuration for React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trips.router)


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Vacation Planner API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Optional: Mount static files for production (React build)
# Uncomment the following lines after building the React app
# frontend_dist = project_root / "frontend" / "dist"
# if frontend_dist.exists():
#     app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")


def run_server():
    """Entry point for running the server via script."""
    import uvicorn
    uvicorn.run(
        "manual_save_to_db.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    run_server()
