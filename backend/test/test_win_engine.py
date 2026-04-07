from models.game_state import GameState
from engine.win_engine import check_game_status, is_game_over


# --- is_game_over tests ---

def test_game_not_over_at_start():
    state = GameState()
    assert is_game_over(state) == False

def test_game_over_when_not_alive():
    state = GameState()
    state.alive = False
    assert is_game_over(state) == True

def test_game_over_when_won():
    state = GameState()
    state.won = True
    assert is_game_over(state) == True

def test_game_over_when_max_days_reached():
    state = GameState()
    state.day = state.MAX_DAYS
    assert is_game_over(state) == True


# --- check_game_status tests ---

def test_lose_when_out_of_money():
    state = GameState()
    state.money = -1
    status, message = check_game_status(state)
    assert status == "lose"
    assert "money" in message.lower()

def test_lose_when_chemistry_negative():
    state = GameState()
    state.chemistry = -1
    status, message = check_game_status(state)
    assert status == "lose"
    assert "chemistry" in message.lower()

def test_win_when_at_final_location_with_full_progress():
    state = GameState()
    state.location_index = 10
    state.product_progress = 100
    status, message = check_game_status(state)
    assert status == "win"
    assert state.won == True

def test_continue_when_at_final_location_but_progress_too_low():
    state = GameState()
    state.location_index = 10
    state.product_progress = 50
    status, message = check_game_status(state)
    assert status == "continue"

def test_lose_when_time_runs_out():
    state = GameState()
    state.day = state.MAX_DAYS
    status, message = check_game_status(state)
    assert status == "lose"
    assert "time" in message.lower()

def test_continue_during_normal_play():
    state = GameState()
    status, message = check_game_status(state)
    assert status == "continue"
