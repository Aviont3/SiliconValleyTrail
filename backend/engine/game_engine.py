# engine/game_engine.py

from engine.choice_engine import apply_choice
from engine.event_engine import pick_event
from engine.win_engine import check_game_status, is_game_over
from engine.travel_engine import travel
from services.crypto_event import fetch_crypto_data, get_revenue_multiplier


def process_turn(state, choice):
    if is_game_over(state):
        return state.to_dict(), {"status": "game_over", "message": "The game has already ended."}

    if choice == "travel":
        result = travel(state)
        if not result.get("success", False):
            return state.to_dict(), {"status": "error", "message": result.get("message")}
        event = result.get("travel_event")
    else:
        result = apply_choice(state, choice)
        if not result.get("success", False):
            return state.to_dict(), {"status": "error", "message": result.get("message")}
        state.advance_day()
        event = None

    
    state.turns_since_revenue += 1

    # Collect revenue if interval has passed, scaled by live crypto market
    revenue = state.calculate_revenue()
    crypto_event = None
    if revenue > 0:
        crypto_data = fetch_crypto_data()
        multiplier, crypto_message = get_revenue_multiplier(crypto_data)
        state.money += int(revenue * multiplier)
        crypto_event = {"message": crypto_message, "multiplier": multiplier}

    status, status_message = check_game_status(state)
    if status == "lose":
        state.alive = False
    elif status == "win":
        state.won = True

    return state.to_dict(), {
        "action": result,
        "event": event,
        "crypto_event": crypto_event,
        "status": status,
        "message": status_message,
    }

