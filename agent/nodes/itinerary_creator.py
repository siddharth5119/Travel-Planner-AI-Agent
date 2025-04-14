from typing import Dict, Any
from datetime import datetime, timedelta

def create_itinerary(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates day-by-day itinerary only if destinations exist
    """
    # Safe check for empty destinations
    if not state.get("recommended_destinations"):
        return {
            "itinerary": {},
            "conversation_history": [
                *state.get("conversation_history", []),
                {"role": "system", "content": "No itinerary generated - no matching destinations"}
            ]
        }
    
    destination = state["recommended_destinations"][0]  # Now safe to access
    duration = state["preferences"].get("duration", 3)  # Default 3 days
    trip_type = state["preferences"].get("trip_type", "general")
    
    itinerary = {
        "destination": f"{destination['name']}, {destination['country']}",
        "duration_days": duration,
        "start_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "daily_plan": _generate_daily_activities(destination, duration, trip_type)
    }
    
    return {
        "itinerary": itinerary,
        "conversation_history": [
            *state.get("conversation_history", []),
            {"role": "system", "content": f"Generated {duration}-day itinerary"}
        ]
    }

def _generate_daily_activities(dest: Dict[str, Any], days: int, trip_type: str) -> list:
    """Safe activity generation with defaults"""
    base_activities = {
        "beach": ["Beach relaxation", "Water sports", "Sunset viewing"],
        "city": ["City tour", "Museum visit", "Local dining"],
        "cultural": ["Historical sites", "Cultural show", "Local market"],
        "business": ["Client meetings", "Working lunch", "Networking event"],
        "general": ["Guided tour", "Local exploration", "Free time"]
    }.get(trip_type.lower(), ["Exploring the area"])

    return [{
        "day": day,
        "morning": f"{base_activities[0]} in {dest['name']}",
        "afternoon": f"{base_activities[1]} at {dest.get('top_attraction', 'local areas')}",
        "evening": base_activities[2]
    } for day in range(1, days+1)]