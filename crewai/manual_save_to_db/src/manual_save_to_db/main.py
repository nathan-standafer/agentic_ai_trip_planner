#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from manual_save_to_db.crew import ManualSaveToDb

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
        "The departure date is Wednesday Feb 25, 2026, returning Saturday March 7.  The arrival date in Tokyo is Thursday Feb 26, 2026.",
        "Flights have already been purchased. Departing Columbus Ohio (CMH) Feb 25 at 10:20AM, arriving in Tokyo (HND) Thursday Feb 26 at 5:45PM on Delta flight DL0275. The Return flight is March 7, departing Tokyo at 4:15 PM (Delta flight DL0274), returning to CMH at 11:00 PM.",
        "Hotel reservations have already been made at the karaksa hotel TOKYO STATION. Check-in on Feb 26, check-out on March 3. We will need a hotel for March 3 to March 7 in the Kyoto/Osaka area.",
        "One family member (Nathan) will be running the Tokyo Marathon on Sunday March 1, 2026.  The marathon starts at 9:10AM from the Tokyo Metropolitan Government Building.  Laura and Lydia can do other activities that day while Nathan is running the marathon.",
        "2026 is not a leap year, so the last day of Febuary is Feb 28.",
        "The family wants to take the train from Tokyo to visit Kyoto and Osaka on March 3 and spend the rest of the vacation in that area, returning to Tokyo (HND) on March 7 to return home."
        "Lydia's interests are Anime, Manga, cats, and Japanese food.",
    ]

    trip_considerations = "; ".join(trip_considerations_list)

    activities_considerations_list = [
        "The family wants to do a Mt. Fuji. day trip",
        "The family wants to do the Street Go-Kart Tour in Tokyo, Japan",
        "The family wants to visit the Ghibli Museum in Mitaka, Tokyo.",
        "The family wants to visit the metropolitan government building in Shinjuku to see the city from above.",
        "The family wants to slide down the tsuten-kaku tower in Osaka.",
        #"The family wants to rent kimonos for a photo shoot.",
        "The family wants to visit the meiji shrine in Tokyo.",
        "The family wants to visit the Tokyo sky tree",
        "The female family members want to make coin jewelry while Nathan goes off to run the marathon.",
        #"The family wants to do the sumo experience in Tokyo.",
        "The family wants to visit the nara deer park.",
        "The family wants to visit second street in osaka for shopping.",
        "The family wants to visit the following areas for shopping and sightseeing: akihabara, don quijote stores, mega donki store, muji shopping, book-off stores",
        "The family wants to visit shibuya sky evening visit is desired.",
    ]

    activity_considerations = "; ".join(activities_considerations_list)

    food_considerations_list = [
        "ghibli cafe",
        "godaime hanayama udon",
        "harajuku goyza ru is a desired food location.",
        "pizza marumo in Tokyo is a desired food location.",
        "ginza happo-shinjuku is a desired food location.",
        "The family wants to visit mufusand cat cafe in shinjuku",
    ]

    food_considerations = "; ".join(food_considerations_list)
  
    inputs = {
        'location': 'Tokyo, Kyoto, and Osaka',
        'arrival_date': '2026-02-26',
        'departure_date': '2026-03-07',
        'trip_considerations': trip_considerations,
        'activity_considerations': activity_considerations,
        'food_considerations': food_considerations,
    }

    try:
        ManualSaveToDb().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Tokyo, Japan",
        'current_year': str(datetime.now().year)
    }
    try:
        ManualSaveToDb().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ManualSaveToDb().crew().replay(task_id=sys.argv[1])

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
        ManualSaveToDb().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

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
        result = ManualSaveToDb().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
