import re
from typing import Dict, Any

def handle_followup(state: Dict[str, Any]) -> Dict[str, Any]:
    """Robust modification handler with proper state merging"""
    user_input = state["user_input"].lower()
    updates = {}
    response = ""

    # Duration change detection
    if "day" in user_input or "week" in user_input:
        try:
            if "week" in user_input:
                weeks = int(re.search(r'(\d+)\s*week', user_input).group(1))
                updates["duration"] = weeks * 7
                response = f"✓ Duration updated to {weeks} weeks ({weeks*7} days)"
            else:
                days = int(re.search(r'(\d+)\s*day', user_input).group(1))
                updates["duration"] = days
                response = f"✓ Duration updated to {days} days"
        except (AttributeError, ValueError):
            response = "❗ Please specify like: '5 days' or '2 weeks'"

    # Preserve existing state while applying updates
    return {
        **state,  # Critical: Merge existing state
        "preferences": {
            **state.get("preferences", {}),
            **updates
        },
        "response": response,
        "needs_replan": bool(updates),
        "recommended_destinations": [],
        "itinerary": {}
    } if updates else {
        **state,
        "response": "I can help modify:\n- Duration\n- Budget\n- Destination",
        "needs_followup": True
    }