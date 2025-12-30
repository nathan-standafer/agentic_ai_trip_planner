use uv to install crew (after activating your UV environment):
```uv tool install crewai```

create a new project:
```crewai create crew basic_trip_planner_crew```

```
(agentic_ai_trip_planner) (base) nathan@Nathan-Mint:/media/nathan/linux_ssd/github/agentic_ai_trip_planner/crewai/basic_trip_planner$ crewai create crew basic_trip_planner_crew
Creating folder basic_trip_planner_crew...
Cache expired or not found. Fetching provider data from the web...
Downloading  [####################################]  1126995/57691
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. nvidia_nim
5. groq
6. huggingface
7. ollama
8. watson
9. bedrock
10. azure
11. cerebras
12. sambanova
13. other
q. Quit
Enter the number of your choice or 'q' to quit: 1
Select a model to use for Openai:
1. gpt-4
2. gpt-4.1
3. gpt-4.1-mini-2025-04-14
4. gpt-4.1-nano-2025-04-14
5. gpt-4o
6. gpt-4o-mini
7. o1-mini
8. o1-preview
q. Quit
Enter the number of your choice or 'q' to quit: 6
Enter your OPENAI API key (press Enter to skip): sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
API keys and model saved to .env file
Selected model: gpt-4o-mini
  - Created basic_trip_planner_crew/.gitignore
  - Created basic_trip_planner_crew/pyproject.toml
  - Created basic_trip_planner_crew/README.md
  - Created basic_trip_planner_crew/knowledge/user_preference.txt
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/__init__.py
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/main.py
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/crew.py
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/tools/custom_tool.py
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/tools/__init__.py
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/config/agents.yaml
  - Created basic_trip_planner_crew/src/basic_trip_planner_crew/config/tasks.yaml
Crew basic_trip_planner_crew created successfully!
```

LLM's can be added to crew easily.  Examples:
```
llm = LLM(model="openai/gpt4o-mini")
llm = LLM(model="gemini-2-0-flash")
llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
```

I made some udpates to user_preferences.txt, agents.yaml, and tasks.yaml to ask the agents to create a trip plan.

The agents can be kicked off by running ```crewai run``` from the terminal

Note:  CrewAI will automatically utilize UV behingd the scenes.  If I activate the UV environment created for teh OpenAI Agents SDK, it seem to conflice with crew.  I think the best approach is to not manualy activate the UV environment and let crew take care of it.

After running the agents, here is the final output:

## Detailed Itinerary for a Vacation to Tokyo, Japan

### Day 1: Arrival and Shibuya Exploration
- **Morning: Arrival at Narita/Haneda Airport**
  - Transfer to your hotel in Shibuya. Check in and freshen up.
  
- **Afternoon: Shibuya Crossing**
  - Walk to the famous Shibuya Crossing. Experience the organized chaos as hundreds of people criss-cross this intersection simultaneously. Perfect for a photo opportunity!
  - Have lunch at a nearby café or a local izakaya (Japanese pub).

- **Evening: Dinner and Shopping in Shibuya**
  - Explore shopping options in Shibuya 109, a trendy shopping mall for fashion enthusiasts.
  - For dinner, try local ramen at Ichiran Ramen, known for its delicious tonkotsu broth.
   
### Day 2: Cultural and Historical Sites
- **Morning: Meiji Shrine**
  - After breakfast, head to the serene Meiji Shrine, dedicated to Emperor Meiji and Empress Shoken, nestled in a lush forest.
  
- **Afternoon: Asakusa and Senso-ji Temple**
  - Visit Tokyo’s oldest temple, Senso-ji. Walk through the Nakamise shopping street, where you can sample traditional snacks, like melon bread and kaminari-okoshi (rice crisps).
  - Enjoy lunch at a local restaurant around Senso-ji.

- **Evening: Sumida River Cruise**
  - Embark on an evening cruise along the Sumida River, taking in the beautiful skyline views of Tokyo illuminated at night. 

### Day 3: Modern Experiences and Shopping
- **Morning: Akihabara**
  - Dive into the otaku culture in Akihabara. Visit shops specializing in anime, manga, and electronics, and don't miss the themed cafés.

- **Afternoon: Odaiba**
  - Grab lunch in Akihabara before heading to Odaiba. Explore the giant Gundam statue and visit TeamLab Borderless, an immersive digital art museum known for its stunning light exhibits.
  
- **Evening: Dinner in Odaiba**
  - Have dinner at DiverCity Tokyo Plaza, where you’ll find a variety of dining options with a view of the Rainbow Bridge. 

### Day 4: Parks and Urban Nature
- **Morning: Ueno Park**
  - Head to Ueno Park, where you can stroll through expansive gardens. Visit the Ueno Zoo or one of the museums, such as the Tokyo National Museum.

- **Afternoon: Shinjuku Gyoen National Garden**
  - Afterward, visit Shinjuku Gyoen, a blend of traditional Japanese, French, and English-style gardens. Enjoy a peaceful walk and perhaps a picnic lunch in the park. 

- **Evening: Robot Restaurant**
  - Experience the unique dining and entertainment at the Robot Restaurant in Shinjuku. Witness high-energy performances of robots, neon lights, and music. 

### Day 5: Theme Parks and City Views
- **Morning: Tokyo Disneyland**
  - Spend the day at Tokyo Disneyland. Enjoy various attractions and character experiences. Be sure to try the popcorn in unique flavors offered throughout the park!

- **Evening: Tokyo Skytree**
  - After a day of fun, visit Tokyo Skytree in the late afternoon. Ascend to the observation deck for breathtaking views of the metropolis and beyond as the sun sets.

### Day 6: Shopping and Culinary Delights
- **Morning: Ginza Shopping District**
  - Enjoy a leisurely breakfast in your hotel or at a café and then head to Ginza for luxury shopping. Visit flagship stores and unique boutiques.

- **Afternoon: Tsukiji Outer Market**
  - Head to the Tsukiji Outer Market for lunch. Sample fresh seafood and traditional Japanese street food, including grilled seafood and fresh sushi.

- **Evening: Farewell Dinner**
  - Conclude your Tokyo adventure with a fine dining experience at one of Ginza's gourmet restaurants, indulging in kaiseki (traditional multi-course Japanese meal).

### Day 7: Departure
- **Morning: Final Exploration**
  - Depending on your flight timing, you might want to visit any last attraction or do last-minute shopping.

- **Afternoon: Check out and Head to the Airport**
  - Transfer to Narita or Haneda Airport for your departure. Safe travels!

Enjoy your unforgettable journey to Tokyo, immersing yourself in the city’s vibrant culture, exquisite cuisine, and unique attractions!
