

def is_game_over(state):
    return not state.alive or state.won or state.day >= state.MAX_DAYS


def check_game_status(state):
    if state.money < 0:
        return "lose", "You ran out of money!"
    if state.chemistry < 0:
        return "lose", "Your chemistry is too low!"
    if state.day >= state.MAX_DAYS:
        return "lose", "Time's up! You didn't build a successful startup in time."
    if state.location_index >= 10 and state.product_progress >= 100:
        state.won = True
        return "win", "Congratulations! You've built a successful startup!"
    if state.location_index >= 10 and state.product_progress < 100:
        return "continue", "You reached San Francisco, but you're not ready yet. Keep building!"

    return "continue", "Keep going."
