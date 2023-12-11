import json
import logging
import os
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS
from src.game_data import extract_game_data
from src.phase import handle_phase


app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
logging.basicConfig(level=logging.INFO)


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
            print(response)
            socketio.emit('game_state_update', response, room=steamid)

        return 'OK', 200
    except Exception as e:
        print(f"Error processing game state update: {e}")
        return 'Error', 500


@socketio.on('connect')
def handle_connect():
    print("User connected")
    # No need to join a room immediately; wait for the SteamID to be sent


@socketio.on('connect_with_steamid')
def handle_connect_with_steamid(data):
    steamid = data.get('steamid')
    join_room(steamid)
    print(f"User connected with SteamID: {steamid}")
    socketio.emit('connected', {'message': 'Successfully connected'}, room=steamid)


@socketio.on('disconnect')
def handle_disconnect():
    steamid = request.args.get('room_name')
    print(f"User disconnected with SteamID: {steamid}")
    if steamid:
        leave_room(steamid)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    socketio.run(app, port=port)


