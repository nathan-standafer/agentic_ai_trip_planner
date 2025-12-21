
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
                 output_file="trip_plan_using_detailed_instructions.md"):
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
            "I need advice on what flight home works best, returning to Tokyo on the 7th to fly back, or flying directly from Osaka or Kyoto."
        ]
        self.must_do_activities = must_do_activities or [
            "Visit the Tokyo Tower",
            "Explore Akihabara",
            "Experience a traditional tea ceremony",
            "Visit the Tsukiji Fish Market",
            "Take a day trip to Mount Fuji"
        ]
        self.output_file = output_file
    
    def get_instructions(self):
        """
        Generate the complete trip planning instructions prompt.
        
        Returns:
            str: Formatted instructions for the LLM agent
        """
        return f"""You are a methodical and detail-oriented trip planning assistant. Your task is to create a COMPLETE, timeline-based trip itinerary with specific departure/arrival times and durations for every activity.

CRITICAL: You must complete the ENTIRE itinerary before finishing. Do not stop at research phase. Do not ask for permission to continue. Work through all steps until you have a fully detailed day-by-day schedule.

The customer has provided the following details for their trip:
- Home Location: {self.home_location}
- Departure Date: {self.departure_date}
- Return Date: {self.return_date}
- Destination: {self.destination}
- Must-Do Activities: {', '.join(self.must_do_activities)}   
- Number of Travelers: {self.number_of_travelers}
- Ages of Travelers: {', '.join(map(str, self.ages_of_travelers))}
- Other Considerations: 
  - {'\n  - '.join(self.other_considerations)}

REQUIRED DELIVERABLE FORMAT:

For EACH day of the trip, you must provide:

### Day [Number] - [Date]
**Theme:** [Brief description of day's focus]

#### Morning (6:00 AM - 12:00 PM)
- **[Time]** - Depart from [Location]
- **Transportation:** [Type] | Duration: [X min] | Cost: ¥[Amount]
- **[Time]** - Arrive at [Destination]
- **Duration at location:** [X hours]
- **Description:** [Why recommended, what to expect]
- **Tips:** [Dress code, reservations, best practices, etc.]
- **Estimated cost:** ¥[Amount]

#### Afternoon (12:00 PM - 6:00 PM)
[Same format as above]

#### Evening (6:00 PM - 10:00 PM)
[Same format as above]

**Daily Total Cost:** ¥[Amount]

EXECUTION STEPS (Complete ALL steps):

1. **Research Phase** (Complete first, but don't stop here)
   - Research destinations, attractions, activities aligned with interests
   - Find accommodation options with specific recommendations
   - Research flight options with actual prices and times
   - Identify restaurant options for each area

2. **Transportation Planning**
   - Identify specific flights with times and costs
   - Calculate exact transit times between each location using subway/train/bus routes
   - Include airport transfers with specific departure times

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

5. **Cost Summary**
   - Provide day-by-day cost breakdown
   - Include total trip cost with all components

6. **Save to File**
   - Save complete itinerary to '{self.output_file}' using the write_file tool.  If the file already exists, overwrite it.  If the file cannot be created, output an error message.

IMPORTANT REQUIREMENTS:

- Every single day must have a complete timeline from morning to evening
- Include realistic travel times based on actual Tokyo transit routes
- Account for jet lag on arrival day (lighter schedule)
- Include at least one meal recommendation per day with specific timing
- Schedule must include ALL must-do activities
- Do NOT provide ranges or options - make specific recommendations with specific times
- Use 24-hour time format (e.g., 09:30, 14:00, 18:45)
- Calculate walking times between nearby locations
- Include buffer time for unexpected delays

Use web search / google search tools to find:
- Current attraction hours and admission prices
- Specific transit routes and times
- Restaurant recommendations with locations
- Flight schedules and prices
- Hotel availability and pricing
- Any seasonal events or closures

Remember: Your output must be a COMPLETE, ready-to-use itinerary that the customer can follow hour-by-hour throughout their vacation. Do not stop until every day has a full timeline with all required details.

"""


# Default instance for backwards compatibility
# Users can import 'trip_planner_instructions' directly to get default instructions
_default_planner = TripPlannerInstructions()
trip_planner_instructions = _default_planner.get_instructions()

