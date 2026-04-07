from data.locations import LOCATIONS
from data.locations_choices import LOCATION_CHOICES

DEFAULT_CHOICES = {
    "build": {
        "label": "Work on product",
        "effects": {"money": -100, "product_progress": 10}
    },
    "eat": {
        "label": "Take a team break",
        "effects": {"money": -30, "chemistry": 8}
    },
    "market": {
        "label": "Run a generic campaign",
        "effects": {"money": -80, "followers": 80}
    }
}


def get_available_choices(state):
    """Get available choices for the current location."""
    if state.location_index < 0 or state.location_index >= len(LOCATIONS):
        return []

    location = LOCATIONS[state.location_index]
    location_data = LOCATION_CHOICES.get(location, DEFAULT_CHOICES)

    choices = []
    for choice_key, choice_data in location_data.items():
        choices.append({
            "key": choice_key,
            "label": choice_data["label"],
            "effects": choice_data["effects"]
        })
    return choices


def apply_choice(state, choice):
    if state.location_index < 0 or state.location_index >= len(LOCATIONS):
        return {"success": False, "message": "Invalid location."}

    location = LOCATIONS[state.location_index]
    location_data = LOCATION_CHOICES.get(location, DEFAULT_CHOICES)

    if choice not in location_data:
        return {"success": False, "message": "Invalid choice."}

    selected = location_data[choice]
    state.apply_effects(selected["effects"])

    return {
        "success": True,
        "choice": choice,
        "label": selected["label"],
        "effects": selected["effects"],
        "location": location,
    }
