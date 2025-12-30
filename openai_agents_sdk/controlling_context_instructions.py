
class TripPlannerInstructions:
    """
    A class to generate trip planning instructions for an LLM agent.
    
    Allows using default values or overriding them with custom parameters.
    
    Example usage:
        # Use defaults
        instructions = TripPlannerInstructions()
        prompt = instructions.get_instructions()
        
        # Override specific values
        instructions = TripPlannerInstructions(
            home_location="New York, NY",
            destination="Paris, France"
        )
        prompt = instructions.get_instructions()
    """
    
    def __init__(self,
                 home_location="Columbus, OH",
                 departure_date="2026/02/25",
                 return_date="2026/03/07",
                 destination="Tokyo, Japan",
                 number_of_travelers=3,
                 ages_of_travelers=None,
                 other_considerations=None,
                 must_do_activities=None,
                 output_file=None):
        """
        Initialize trip planner with parameters.
        
        Args:
            home_location: Starting location for the trip
            departure_date: Date of departure (YYYY/MM/DD format)
            return_date: Date of return (YYYY/MM/DD format)
            destination: Trip destination
            number_of_travelers: Number of people traveling
            ages_of_travelers: List of ages of travelers
            other_considerations: List of special considerations or requirements
            must_do_activities: List of activities that must be included
        """
        self.home_location = home_location
        self.departure_date = departure_date
        self.return_date = return_date
        self.destination = destination
        self.number_of_travelers = number_of_travelers
        self.ages_of_travelers = ages_of_travelers or [51, 50, 17]
        self.other_considerations = other_considerations or [
            "I will be running in the Tokyo marathon on Sunday March 1, so I only need a relaxing place to eat on that day.",
            "Starting on March 3, throughout the rest of the vacation, we want to travel to Kyoto and Osaka.",
            "I need advice on what flight home works best, returning to Tokyo on the 7th to fly back, or flying directly from Osaka or Kyoto.",
            "I already purchased airfare, Departing Columbus at 3:45 PM on Feb 25, arriving in Tokyo HND at 5:45 PM on Feb 26 and departing from HND on Mar 7 at 5:45 PM, arriving in Columbus at 7:15 PM on Mar 7.",
            "I have reservations to stay at karaksa hotel TOKYO STATION Feb 25 - Mar 3."
        ]
        self.must_do_activities = must_do_activities or [
            "Visit the Tokyo Tower",
            "Explore Akihabara",
            "Experience a traditional tea ceremony",
            "Visit the Tsukiji Fish Market",
            "Take a day trip to Mount Fuji"
        ]
        self.output_file = output_file
    
    def get_instructions_for_activities_expert(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the activities expert LLM agent
        """
        return f"""You are a methodical and detail-oriented trip planning assistant. Your task is to create a list of activities for each day of the trip for the relevant location."""
    
    def get_instructions_for_transportation_expert(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the transportation expert LLM agent
        """
        return f"""You are a methodical and detail-oriented trip planning assistant. Your task is to update the given itinerary with detailed transportation options between locations, including specific train/subway/bus lines, departure times, durations, and costs."""


    def get_instructions_for_trip_evaluation_expert(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the trip evaluation expert LLM agent
        """
        return f"""You are a methodical and detail-oriented trip planning assistant. Your task is to evaluate the given trip plan and provide feedback on the clarity and completeness of the plan, specifically focusing on transportation details."""

    def get_instructions_for_accommodations_expert(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the LLM agent
        """
        return """You are a methodical and detail-oriented trip planning assistant. Your task is to provide accommodation recommendations for the trip based on the provided details."""

    def get_instructions_for_dining_expert(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the LLM agent
        """
        return f"""You are a methodical and detail-oriented trip planning assistant. Your task is to provide food and dining recommendations for the trip based on the provided details."""
    
    def get_instructions_for_plan_saver(self):
        """
        Generate the complete trip planning instructions for the save tool.
        
        Returns:
            str: Formatted instructions for the LLM agent
        """
        return f"""You are a reliable assistant that will save a given json-based text string that represents a trip plan to disk.  You will make the necessary formatting updates to the file to ensure it is valid json, then use the write_file tool to save to this location: {self.output_file}"""

    def get_instructions_for_manager(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the LLM agent
        """
        return f"""You are a methodical and detail-oriented trip planning assistant. Your task is to create a COMPLETE, timeline-based trip itinerary with specific departure/arrival times and durations for every activity.

You will have several tools at your disposal to help you complete this task.  Use the tools repeatedly as needed to gather information and refine the itinerary. The tools available to you are:
1. Activities_Expert_Agent: Provide this tool with an "input" that describes the Location, date, the ages of the travels, and other relevant inforation. The tool will return a list of recommended activities and attractions for that location on that date.
2. Transportation_Expert_Agent: Provide this tool with an "input" that describes the a starting, destination location and time of day.  The tool will provide transportation options between locations, including specific train/subway/bus lines, departure times, durations, and costs.
3. Trip_Evaluation_Expert_Agent: Provide the current trip plan in json format and this tool will evaluate the plan and provide feedback on the clarity and completeness of the plan.
4. Accommodations_Expert_Agent: Provide this tool with an "input" that describes the Location and date range.  The tool will return accommodation recommendations for that location during that time period.
5. Dining_Expert_Agent:  Provide this tool with an "input" that describes the a location, day of the week, and time range to find the best dining optins for a specific time and location in th trip plan.
6. Plan_Save_Agent: Provide this tool with the final json output representing the trip plan.  The tool will save the trip plan to local stoage to share with the travelers.


CRITICAL: You must complete the ENTIRE itinerary before finishing. Do not stop at research phase. Do not ask for permission to continue. Work through all steps until you have a fully detailed day-by-day schedule.

The customer has provided the following details for their trip:
- Home Location: {self.home_location}
- Departure Date: {self.departure_date}
- Return Date: {self.return_date}
- Destination: {self.destination}
- Must-Do Activities: {self.must_do_activities}   
- Number of Travelers: {self.number_of_travelers}
- Ages of Travelers: {self.ages_of_travelers}
- Other Considerations: 
  - {'\n  - '.join(self.other_considerations)}

REQUIRED DELIVERABLE FORMAT:

The final itinerary must be formatted as follows for EACH DAY of the trip in JSON format:
{{
  "tripPlan": {{
    "title": "Complete Tokyo & Kansai Region Trip Itinerary",
    "startDate": "2026-02-25",
    "endDate": "2026-03-07",
    "currency": "JPY",
    "travelers": 3,
    "days": [
      {{
        "dayNumber": 1,
        "date": "2026-02-25",
        "theme": "Arrival & Jet Lag Recovery",
        "dailyTotalCost": 2800,
        "activities": [
          {{
            "time": "15:45",
            "activity": "Depart Columbus",
            "location": "Columbus Airport",
            "transportation": null,
            "duration": null,
            "cost": null,
            "details": "Flight from Columbus Airport"
          }},
          {{
            "time": "17:45",
            "activity": "Arrive Tokyo HND",
            "location": "Haneda Airport",
            "transportation": {{
              "type": "Limousine Bus",
              "details": "Take from Terminal 1 Stop 4 or Terminal 2 Stop 6"
            }},
            "duration": "1h 20m",
            "cost": 1300,
            "details": "Take from Terminal 1 Stop 4 or Terminal 2 Stop 6"
          }},
          {{
            "time": "19:05",
            "activity": "Arrive Tokyo Station Yaesu",
            "location": "Tokyo Station Yaesu",
            "transportation": {{
              "type": "Walk",
              "details": null
            }},
            "duration": "5 min",
            "cost": 0,
            "details": "Head to karaksa hotel"
          }},
          {{
            "time": "19:10",
            "activity": "Check-in karaksa hotel",
            "location": "karaksa hotel",
            "transportation": null,
            "duration": "30 min",
            "cost": null,
            "details": "Address: 1-5-3 Yaesu, Chuo-ku"
          }},
          {{
            "time": "19:40",
            "activity": "Light dinner nearby",
            "location": "Near hotel",
            "transportation": {{
              "type": "Walk",
              "details": null
            }},
            "duration": "15 min",
            "cost": 1500,
            "details": "Convenience store or small restaurant"
          }},
          {{
            "time": "20:30",
            "activity": "Return to hotel",
            "location": "karaksa hotel",
            "transportation": {{
              "type": "Walk",
              "details": null
            }},
            "duration": "5 min",
            "cost": 0,
            "details": "Early rest to combat jet lag"
          }},
          {{
            "time": "21:00",
            "activity": "Sleep",
            "location": "karaksa hotel",
            "transportation": null,
            "duration": null,
            "cost": null,
            "details": "Adjust to Japan time"
          }}
        ],
        "diningRecommendations": [
          {{
            "name": "Lawson Convenience Store",
            "location": "2 min walk from hotel",
            "mealTime": "19:40",
            "cuisine": "Bento/Sushi",
            "costPerPerson": 800,
            "whyRecommended": "Fresh Japanese food, open 24 hours"
          }},
          {{
            "name": "Sukiya",
            "location": "Yaesu Exit area",
            "mealTime": "19:30",
            "cuisine": "Gyudon",
            "costPerPerson": 700,
            "whyRecommended": "Famous beef bowl chain, quick service"
          }}
        ]
      }}
    ],
    "accommodations": [
      {{
        "name": "karaksa hotel",
        "address": "1-5-3 Yaesu, Chuo-ku",
        "city": "Tokyo",
        "checkIn": "2026-02-25",
        "checkOut": "2026-03-04"
      }},
      {{
        "name": "Kyoto Hotel",
        "address": "123 Kyoto St, Shimogyo-ku",
        "city": "Kyoto",
        "checkIn": "2026-03-04",
        "checkOut": "2026-03-07"
      }}
    ],
    "summary": {{
      "totalCostPerPerson": 111260,
      "totalCostAllTravelers": 333780,
      "approximateUSD": 741,
      "exchangeRate": 150,
      "dailyCosts": [
        {{ "day": 1, "cost": 2800 }},
        {{ "day": 2, "cost": 6540 }},
        {{ "day": 3, "cost": 8560 }}
      ],
      "transportationSummary": [
        {{ "category": "Tokyo local transport", "costPerPerson": 2000 }},
        {{ "category": "Shinkansen Tokyo-Kyoto", "costPerPerson": 14000 }},
        {{ "category": "Shinkansen Kyoto-Osaka-Tokyo", "costPerPerson": 16840 }},
        {{ "category": "Airport transfers", "costPerPerson": 1800 }}
      ]
    }},
    "keyRecommendations": [
      "Return to Tokyo from Kyoto on March 7 morning as planned",
      "Book accommodations near Kyoto Station for easy access",
      "Day 6 is designed for gentle activities to aid marathon recovery",
      "Consider JR Pass for Kansai portion (Days 8-10)"
    ],
    "transportationNotes": [
      "Day 1: Limousine Bus runs every 10-15 minutes, allow 1 hour total",
      "Day 6: Modified for marathon recovery with reduced walking",
      "Day 7: Mount Fuji 5th Station may be closed in March - alternative to Lake Kawaguchiko",
      "Day 11: 8:00 AM Shinkansen provides 3+ hour buffer for 5:45 PM flight"
    ]
  }}
}}

EXECUTION STEPS (Complete ALL steps):

1. **Research Phase** (Complete first, but don't stop here)
   - Research destinations, attractions, activities aligned with interests
     * Utilze the Activities_Expert_Agent for the best results.
   - Find accommodation options with specific recommendations
     * Utilize the Accommodations_Expert_Agent 
   - Research flight options with actual prices and times
     * Utilize the Transportation_Expert_Agent
   - Identify restaurant options for each area
     * Utilize the Dining_Expert_Agent 
   
2. **Transportation Planning**
   - Identify specific flights with times and costs
   - Calculate exact transit times between each location using subway/train/bus routes
   - Include airport transfers with specific departure times
   - Utilze the Transportation_Expert_Agent for the best results.

3. **Daily Itinerary Creation** (THIS IS THE MAIN DELIVERABLE)
   - Create hour-by-hour schedule for EACH of the 9 days (Feb 25 - Mar 5)
   - Include specific times for: wake up, depart hotel, arrive at location, depart location, meal times, return to hotel
   - For transportation between each location, specify:
     * Departure time and location
     * Transport type (JR line name, subway line, bus route, etc.)
     * Duration (in minutes)
     * Cost per person
     * Arrival time and location
   - For each activity/location, specify:
     * Arrival time
     * Duration of visit (in hours/minutes)
     * Entry costs
     * Description (2-3 sentences on what to do/see)
     * Important tips (reservations needed, dress code, best times, etiquette, what to bring)

4. **Dining Recommendations**
   - For each day, recommend 2-3 specific restaurants with:
     * Name and location
     * Suggested meal time
     * Expected cost per person
     * Type of cuisine
     * Why recommended
  - Utilize the Dining_Expert_Agent

5. **Cost Summary**
   - Provide day-by-day cost breakdown
   - Include total trip cost with all components

6. **Evaluation**
   - After completing the itinerary, use the Trip_Evaluation_Expert_Agent to review the entire plan.  
   - If the Trip_Evaluation_Expert_Agent provides feedback, revise the itinerary accordingly and re-submit for evaluation.
   - If the Trip_Evaluation_Expert_Agent indicates the plan is clear, Include the evaluation feedback summary at the end of the itinerary and proceed to step 7.  
   
7. **Save to File**
   - Save complete itinerary to '{self.output_file}' using the Plan_Save_Agent tool.  
   - This is the final deliverable and is CRITICAL to the success of the trip planning process.


IMPORTANT REQUIREMENTS:
- Every single day must have a complete timeline from morning to evening
- Include realistic travel times based on actual transit routes
- Account for jet lag on arrival day (lighter schedule)
- Include at least two meal recommendations per day with specific timing
- Schedule must include ALL must-do activities
- Do NOT provide ranges or options - make specific recommendations with specific times
- Calculate walking times between nearby locations
- Include buffer time for unexpected delays
- Be sure to be use precise names when calling other tools.  This is extremely important as calling an agent with an incorrect name will result in errors. The only relevant tools names are as follows.  Do not call a tool that is not in this list:
  * Activities_Expert_Agent
  * Transportation_Expert_Agent
  * Trip_Evaluation_Expert_Agent
  * Accommodations_Expert_Agent
  * Dining_Expert_Agent
  * Plan_Save_Agent

Use available tools to find:
- Current attraction hours and admission prices
- Specific transit routes and times
- Restaurant recommendations with locations
- Flight schedules and prices
- Hotel availability and pricing
- Any seasonal events or closures

Remember: Your output must be a COMPLETE, ready-to-use itinerary that the customer can follow hour-by-hour throughout their vacation. Do not stop until every day has a full 
timeline with all required details.  Complete ALL steps including evaluation and saving the itenerary (Step 7) before finishing. Always end your final response with the 
exact token: <TASK_COMPLETE>.
"""



