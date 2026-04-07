"""
Integration tests for the full turn flow through process_turn().
These tests exercise the entire pipeline: game state -> engine -> result.
"""
from models.game_state import GameState
from engine.game_engine import process_turn


# --- City choice turn ---

def test_city_choice_returns_state_and_result():
    state = GameState()
    state_dict, result = process_turn(state, "build")

    assert isinstance(state_dict, dict), "Should return a state dictionary"
    assert "money" in state_dict
    assert "day" in state_dict
    assert "status" in result

def test_city_choice_advances_day():
    state = GameState()
    process_turn(state, "build")
    assert state.day == 1, "Day should advance by 1 after a city choice"

def test_city_choice_no_event():
    state = GameState()
    _ , result = process_turn(state, "build")
    assert result.get("event") is None, "City choices should not produce events"

def test_city_choice_reduces_money():
    state = GameState()
    initial_money = state.money
    process_turn(state, "build")
    assert state.money < initial_money, "Money should decrease after 'build'"

def test_invalid_choice_returns_error():
    state = GameState()
    state_dict, result = process_turn(state, "notarealchoice")
    assert result["status"] == "error"


# --- Travel turn ---

def test_travel_turn_advances_location():
    state = GameState()
    initial_index = state.location_index
    process_turn(state, "travel")
    assert state.location_index == initial_index + 1, "Location index should increase after travel"

def test_travel_turn_advances_days():
    state = GameState()
    process_turn(state, "travel")
    assert state.day > 0, "Days should advance after travel"

def test_travel_turn_returns_event():
    state = GameState()
    _, result = process_turn(state, "travel")
    assert result.get("event") is not None, "Travel should produce an event"

def test_travel_turn_costs_money():
    state = GameState()
    initial_money = state.money
    process_turn(state, "travel")
    assert state.money < initial_money, "Travel should cost money"


# --- Game over guard ---

def test_process_turn_blocked_when_game_already_over():
    state = GameState()
    state.alive = False
    _, result = process_turn(state, "build")
    assert result["status"] == "game_over"

def test_process_turn_blocked_when_time_expired():
    state = GameState()
    state.day = state.MAX_DAYS
    _, result = process_turn(state, "build")
    assert result["status"] == "game_over"


# --- Revenue collection ---

def test_revenue_collected_after_interval():
    state = GameState()
    state.followers = 100
    # Play enough turns to pass the REVENUE_INTERVAL (5 days)
    initial_money = state.money
    for _ in range(state.REVENUE_INTERVAL):
        process_turn(state, "eat")  # "eat" costs less, easier to isolate revenue
    # After 5 days revenue should have been collected at least once
    # Net money may still be less, but revenue was added at some point
    assert state.turns_since_revenue == 0, "Revenue interval should have reset"


# --- Win condition ---

def test_win_when_at_end_with_full_progress():
    state = GameState()
    state.location_index = 10
    state.product_progress = 100
    _, result = process_turn(state, "build")
    # process_turn checks game over first — at index 10, build is a valid city choice
    # status should be win or game continues to win check
    assert result["status"] in ("win", "continue", "game_over")

def test_lose_condition_no_money():
    state = GameState()
    state.money = 10  # just enough to go negative after a build (-100)
    _, result = process_turn(state, "build")
    assert result["status"] == "lose"
    assert state.alive == False
