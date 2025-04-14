import os
from dotenv import load_dotenv
from agent.graph import build_travel_agent
from agent.state import create_initial_state

load_dotenv()

def display_preferences(prefs: dict) -> None:
    """Formatted display of extracted preferences"""
    if not prefs:
        print("\n⚠️ No preferences could be extracted")
        return
        
    print("\n" + "="*50)
    print("🔍 Extracted Travel Preferences")
    print("-"*50)
    for key, value in prefs.items():
        if isinstance(value, list):
            print(f"{key.replace('_', ' ').title():<20}: {', '.join(value)}")
        else:
            print(f"{key.replace('_', ' ').title():<20}: {value}")
    print("="*50)

def display_destinations(dests: list) -> None:
    """Formatted display of recommended destinations"""
    if not dests:
        print("\n⚠️ No destinations found matching your criteria")
        return
        
    print("\n" + "="*50)
    print("✈️ Recommended Destinations")
    print("-"*50)
    for i, dest in enumerate(dests, 1):
        print(f"\n{i}. {dest['name']}, {dest['country']}")
        print(f"   Type: {dest.get('type', 'N/A')}")
        print(f"   Budget: {dest.get('budget_level', 'N/A')}")
        print(f"   Ideal Duration: {dest.get('ideal_duration', 'N/A')} days")
        if dest.get('keywords'):
            print(f"   Keywords: {', '.join(dest['keywords'])}")
    print("\n" + "="*50)

def display_itinerary(itinerary: dict) -> None:
    """Formatted display of generated itinerary"""
    if not itinerary:
        print("\n⚠️ No itinerary could be generated")
        return
        
    print("\n" + "="*50)
    print("📅 Travel Itinerary")
    print("-"*50)
    print(f"Destination: {itinerary['destination']}")
    print(f"Duration: {itinerary['duration_days']} days")
    print(f"Start Date: {itinerary.get('start_date', 'Not specified')}")
    
    for day in itinerary["daily_plan"]:
        print("\n" + "-"*20)
        print(f"Day {day['day']}:")
        print(f"  ☀ Morning: {day['morning']}")
        print(f"  🌤 Afternoon: {day['afternoon']}")
        print(f"  🌙 Evening: {day['evening']}")
    print("\n" + "="*50)

def main():
    app = build_travel_agent()
    state = create_initial_state()
    
    print("\n=== Travel Planner AI ===")
    print("Say 'modify' to change your trip or 'exit' to quit\n")
    
    while True:
        # Get input based on context
        if state.get("itinerary"):
            user_input = input("\nWhat would you like to modify? ").strip()
            state["needs_followup"] = True
        else:
            user_input = input("\nDescribe your trip: ").strip()
            state = create_initial_state()

        if user_input.lower() in ['exit', 'quit']:
            break
            
        state["user_input"] = user_input
        new_state = app.invoke(state)
        
        # Update state while preserving existing data
        state = {**state, **new_state}
        
        # Display logic
        if "preferences" in state:
            print("\nCurrent Preferences:")
            print(f"- Duration: {state['preferences'].get('duration', 'N/A')} days")
            print(f"- Budget: {state['preferences'].get('budget_level', 'N/A')}")
        
        if "itinerary" in state:
            display_itinerary(state["itinerary"])

if __name__ == "__main__":
    main()