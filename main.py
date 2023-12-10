import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, leave_room

from src.game_data import extract_game_data
from src.phase import handle_phase

# Instantiates Flask
app = Flask(__name__)

# Instantiates Socket
socketio = SocketIO(app)


# Socket Testing on local webpage
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_gsi', methods=['POST'])
def handle_game_state_update():
    try:
        data = request.data.decode('UTF-8')
        json_data = json.loads(data)

        # Extract game data from JSON
        game_data = extract_game_data(json_data)

        # Handle round phase flow
        response = handle_phase(game_data)

        # Get users steamid to join room
        steamid = game_data['steamid']

        # Handle socketing
        if response:
            socketio.emit('game_state_update', response, room=steamid)

        return 'OK', 200
    except Exception as e:
        print(f"Error processing game state update: {e}")
        return 'Error', 500


@socketio.on('connect')
def handle_connect():
    steamid = request.args.get('room_name')  # Get SteamID from the query parameters
    join_room(steamid)
    print(f"User connected with SteamID: {steamid}")


@socketio.on('disconnect')
def handle_disconnect():
    steamid = request.args.get('room_name')
    print(f"User disconnected with SteamID: {steamid}")
    if steamid:
        leave_room(steamid)


if __name__ == '__main__':
    socketio.run(app, port=8888, allow_unsafe_werkzeug=True)
