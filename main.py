import os
from flask import Flask, request, jsonify
from flask_socketio import join_room
from flask_cors import CORS
from src.game_handler import handle_game_state_update
from config.socket_manager import socketio

app = Flask(__name__)
CORS(app, resources={r"/socket.io/*": {"origins": "http://localhost:*"}})
socketio.init_app(app)
connected_steamids = set()
print(f'currently connected {connected_steamids}')


@app.route('/update_gsi', methods=['POST'])
def update_gsi():
    data = request.get_json()
    steamid = data.get('steamid')

    if steamid in connected_steamids:
        return handle_game_state_update(request)
    else:
        response = {'status': 'SteamID not connected', 'message': 'POST received but user not connected to AIGL'}
        print(response['message'])
        return jsonify(response)


@socketio.on('connect_with_steamid')
def handle_connect_with_steamid(data):
    steamid = data.get('steamid')
    join_room(steamid)
    connected_steamids.add(steamid)
    print(f"User connected with SteamID: {steamid}")
    socketio.emit('connected', {'message': 'Successfully connected'}, room=steamid)


@socketio.on('disconnect_with_steamid')
def handle_disconnect_with_steamid(data):
    # Extract the SteamID from the disconnect event
    steamid = data.get('steamid')
    connected_steamids.discard(steamid)
    print(f"User disconnected with SteamID: {steamid}")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    socketio.run(app, port=port)
