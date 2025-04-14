from typing import TypedDict, Dict, List, Any, Union

class AgentState(TypedDict):
    """Core state structure for the travel agent"""
    user_input: str
    preferences: Dict[str, Union[str, int, List[str]]]
    recommended_destinations: List[Dict[str, Any]]
    itinerary: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    needs_followup: bool

def create_initial_state() -> AgentState:
    """Initialize a clean state object"""
    return {
        "user_input": "",
        "preferences": {},
        "recommended_destinations": [],
        "itinerary": {},
        "conversation_history": [],
        "needs_followup": False
    }