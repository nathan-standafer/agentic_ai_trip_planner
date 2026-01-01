#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from manager_agent.crew import ManagerAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    trip_considerations_list = [
        "The family lives in Columbus, OH.",
        "The family has 3 members. Nathan (51), Laura (50), and Lydia (17).",
        "The departure date is Feb 25, 2026, returning March 7.",
        "Flights have already been purchased. Departing Columbus Ohio (CMH) Feb 25 at 10:20AM, arriving in Tokyo (HND) Feb 26 at 5:45PM. The Return flight is March 7, departing Tokyo at 4:15, returning to CMH at 11:00 PM.",
        "Hotel reservations have already been made at the karaksa hotel TOKYO STATION. Check-in on Feb 26, check-out on March 3.",
        "One family member (Nathan) will be running the Tokyo Marathon on Sunday March 1, 2026.",
        "2026 is not leap year, so the last day of Febuary is Feb 28.",
        "The family wants to take the train from Tokyo to visit Kyoto and Osaka on March 3 and spend the rest of the vacation in that area, returning to Tokyo (HND) on March 7 to return home."
    ]
    
    trip_considerations = "; ".join(trip_considerations_list)

    inputs = {
        'location': 'Tokyo, Kyoto, and Osaka',
        'arrival_date': '2026-02-26',
        'departure_date': '2026-03-07',
        'trip_considerations': trip_considerations
    }

    try:
        ManagerAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        ManagerAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ManagerAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        ManagerAgent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = ManagerAgent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
