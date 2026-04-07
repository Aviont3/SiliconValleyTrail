from flask import Flask, request, jsonify
from flask_cors import CORS
from models.game_state import GameState
from engine.game_engine import process_turn
from engine.choice_engine import get_available_choices
from data.start import intro_data

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Global game state (in a real app, use sessions or database)
game_state = None

@app.route('/api/intro', methods=['GET'])
def get_intro():
    return jsonify(intro_data())

@app.route('/api/start', methods=['GET'])
def start_game():
    global game_state
    game_state = GameState()
    choices = get_available_choices(game_state)
    return jsonify({'state': game_state.to_dict(), 'choices': choices})

@app.route('/api/turn', methods=['POST', 'OPTIONS'])
def make_turn():
    global game_state
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if game_state is None:
            return jsonify({'error': 'Game not started'}), 400

        data = request.get_json()
        choice = data.get('choice')
        if not choice:
            return jsonify({'error': 'No choice provided'}), 400

        state_dict, result = process_turn(game_state, choice)
        choices = get_available_choices(game_state)
        return jsonify({
            'state': state_dict,
            'choices': choices,
            'event': result.get('event'),
            'status': result.get('status'),
            'message': result.get('message')
        })
    except Exception as e:
        print(f"Error in make_turn: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)