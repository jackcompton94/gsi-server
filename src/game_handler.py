import json
from main import socketio
from src.phase import handle_phase
from src.game_data import extract_game_data


def handle_game_state_update(request):
    try:
        data = request.data.decode('UTF-8')
        json_data = json.loads(data)

        # Extract game data from JSON
        game_data = extract_game_data(json_data)

        # Get users steamid to join room
        steamid = game_data['steamid']

        # Handle round phase flow
        response = handle_phase(game_data, steamid)

        # Handle socketing
        if response:
            socketio.emit('game_state_update', response, room=steamid)

        return 'OK', 200
    except Exception as e:
        print(f"Error processing game state update: {e}")
        return 'Error', 500