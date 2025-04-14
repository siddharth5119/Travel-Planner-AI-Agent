import json
from typing import Dict, Any, List

def find_destinations(state: Dict[str, Any]) -> Dict[str, Any]:
    """Improved destination finder with better matching and error handling"""
    try:
        # Load destinations with UTF-8 encoding
        with open("data/destinations.json", "r", encoding="utf-8") as f:
            destinations: List[Dict[str, Any]] = json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load destinations: {str(e)}")
        destinations = []

    prefs = state.get("preferences", {})
    matched_destinations = []

    # Flexible matching logic
    for dest in destinations:
        match_score = 0
        
        # Region match (50% weight)
        if prefs.get("region", "").lower() in ["any", dest.get("region", "").lower()]:
            match_score += 50
        
        # Trip type match (30% weight)
        if prefs.get("trip_type", "").lower() == dest.get("type", "").lower():
            match_score += 30
        
        # Keyword matches (10% per keyword)
        for keyword in prefs.get("keywords", []):
            if keyword.lower() in [kw.lower() for kw in dest.get("keywords", [])]:
                match_score += 10
        
        # Duration compatibility (10% if within ideal range)
        ideal_duration = dest.get("ideal_duration", [1, 365])
        if ideal_duration[0] <= prefs.get("duration", 7) <= ideal_duration[1]:
            match_score += 10
        
        if match_score >= 50:  # Minimum threshold
            matched_destinations.append({
                **dest,
                "match_score": match_score
            })

    # Sort by match score (highest first)
    matched_destinations.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "recommended_destinations": matched_destinations[:3],  # Return top 3
        "conversation_history": [
            *state.get("conversation_history", []),
            {"role": "system", "content": f"Found {len(matched_destinations)} potential matches"}
        ]
    }