from models.game_state import GameState
from engine.choice_engine import apply_choice

def test_apply_choice_build_reduces_money_and_increases_progress():
    state = GameState()
    initial_money = state.money
    initial_progress = state.product_progress

    apply_choice(state, "build")
    assert state.money < initial_money, "Money should decrease after 'build' choice"
    assert state.product_progress > initial_progress, "Product progress should increase after 'build' choice"

def test_apply_choice_market_increases_followers():
    state = GameState()
    initial_followers = state.followers

    apply_choice(state, "market")
    assert state.followers > initial_followers, "Followers should increase after 'market' choice"

def test_apply_choice_eat_increases_chemistry():
    state = GameState()
    initial_chemistry = state.chemistry

    apply_choice(state, "eat")
    assert state.chemistry > initial_chemistry, "Chemistry should increase after 'eat' choice"