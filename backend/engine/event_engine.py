import random
from data.events import LOCAL_EVENTS


def pick_event(state, event_pool=None):
    """Pick and apply a random event from a specified event pool."""
    pool = event_pool if event_pool is not None else LOCAL_EVENTS
    event_name, event_data = random.choice(list(pool.items()))
    state.apply_effects(event_data["effects"])
    return {
        "name": event_name,
        "description": event_data.get("description", ""),
        "effects": event_data["effects"],
    }
