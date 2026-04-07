from data.locations import LOCATIONS, ROUTES
from data.events import TRAVEL_EVENTS
from engine.event_engine import pick_event


def travel(state):
    if state.location_index >= len(ROUTES):
        return {
            "success": False,
            "message": "You are already at the final destination.",
            "location": state.get_location_name(),
        }

    route = ROUTES[state.location_index]
    miles = route.get("miles", 0)
    travel_days = max(1, (miles + 99) // 100)
    money_cost = 50 * travel_days
    chemistry_cost = 0.2 * travel_days

    state.money -= money_cost
    state.chemistry -= chemistry_cost
    state.advance_day(travel_days)
    state.location_index += 1

    travel_event = pick_event(state, TRAVEL_EVENTS)

    return {
        "success": True,
        "from": route.get("from"),
        "to": route.get("to"),
        "miles": miles,
        "days": travel_days,
        "money_cost": money_cost,
        "chemistry_cost": chemistry_cost,
        "location_index": state.location_index,
        "location": state.get_location_name(),
        "travel_event": travel_event,
    }

