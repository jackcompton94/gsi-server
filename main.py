import os
from flask import Flask, request
from flask_socketio import join_room
from flask_cors import CORS
from src.game_handler import handle_game_state_update
from config.socket_manager import socketio

app = Flask(__name__)
CORS(app, resources={r"/socket.io/*": {"origins": "http://localhost:*"}})  # Specify the allowed origin
socketio.init_app(app)


@app.route('/update_gsi', methods=['POST'])
def update_gsi():
    return handle_game_state_update(request)


@socketio.on('connect')
def handle_connect():
    print("User connected")


@socketio.on('connect_with_steamid')
def handle_connect_with_steamid(data):
    steamid = data.get('steamid')
    join_room(steamid)
    print(f"User connected with SteamID: {steamid}")
    socketio.emit('connected', {'message': 'Successfully connected'}, room=steamid)


@socketio.on('disconnect')
def handle_disconnect():
    print(f"User disconnected")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    socketio.run(app, port=port)


