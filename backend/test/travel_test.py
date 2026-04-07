from engine.travel_engine import travel
from models.game_state import GameState


def test_travel_advance_location():
    state = GameState()
    initial_index = state.location_index
    travel(state)

    assert state.location_index == initial_index + 1
