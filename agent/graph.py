from langgraph.graph import StateGraph, END
from .state import AgentState

def build_travel_agent():
    workflow = StateGraph(AgentState)
    
    from .nodes.preference_extractor import extract_preferences
    from .nodes.destination_finder import find_destinations
    from .nodes.itinerary_creator import create_itinerary
    from .nodes.followup_handler import handle_followup

    workflow.add_node("extract_preferences", extract_preferences)
    workflow.add_node("find_destinations", find_destinations)
    workflow.add_node("create_itinerary", create_itinerary)
    workflow.add_node("handle_followup", handle_followup)

    # Main flow
    workflow.set_entry_point("extract_preferences")
    workflow.add_edge("extract_preferences", "find_destinations")
    workflow.add_edge("find_destinations", "create_itinerary")

    # Modification handling flow
    workflow.add_conditional_edges(
        "create_itinerary",
        lambda state: "handle_followup" if state.get("needs_followup") else END
    )
    workflow.add_edge("handle_followup", "extract_preferences")

    return workflow.compile()