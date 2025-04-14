from typing import Dict, Any

def extract_preferences(state: Dict[str, Any]) -> Dict[str, Any]:
    input_text = state["user_input"].lower()
    return {
        "preferences": {
            "duration": _extract_duration(input_text),
            "trip_type": _extract_trip_type(input_text),  # "city", "beach" etc.
            "region": _extract_region(input_text),  # "Europe", "Asia" etc.
            "keywords": _extract_keywords(input_text)  # ["business", "luxury"]
        }
    }
def _extract_duration(text: str) -> int:
    # Handle "2 week", "3 days", etc.
    if "week" in text:
        return 7 * int(text[0]) if text[0].isdigit() else 7
    elif "day" in text:
        return int(text[0]) if text[0].isdigit() else 3
    return 7  # default

def _extract_trip_type(text: str) -> str:
    type_priority = [
        ("beach", ["beach", "coast"]),
        ("cultural", ["museum", "culture", "historical"]),
        ("adventure", ["mountain", "hiking", "trekking"]),
        ("city", ["city", "urban", "metropolis"])
    ]
    for t_type, keywords in type_priority:
        if any(kw in text for kw in keywords):
            return t_type
    return "general"

def _extract_region(text: str) -> str:
    regions = {
        "japan": "Asia",
        "europe": "Europe",
        "asia": "Asia",
        "america": "North America",
        "africa": "Africa"
    }
    for country, region in regions.items():
        if country in text:
            return region
    return "any"

def _extract_keywords(text: str) -> list:
    keywords = ["luxury", "budget", "family", "solo", "honeymoon", "business"]
    return [kw for kw in keywords if kw in text]


