import os
from flask import Flask, request, jsonify
from flask_socketio import join_room
from flask_cors import CORS
from src.game_handler import handle_game_state_update
from config.socket_manager import socketio

app = Flask(__name__)

# TODO: update this with the localhost dev URL and aigl-web-app URL
CORS(app, resources={r"/socket.io/*": {"origins": "http://localhost:*"}})
socketio.init_app(app)

connected_steamids = {}


@app.route('/update_gsi', methods=['POST'])
def update_gsi():

    data = request.get_json()
    player_data = data.get('player', {})
    steamid = player_data.get('steamid')

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

    connected_steamids[steamid] = {'username': f'{data.get("name")}'}
    print(f"User connected with SteamID: {steamid}")
    socketio.emit('connected', {'message': 'Successfully connected'}, room=steamid)


@socketio.on('disconnect_with_steamid')
def handle_disconnect_with_steamid(data):

    # Extract the SteamID from the disconnect event
    steamid = data.get('steamid')
    del connected_steamids[f'{steamid}']
    print(f"User disconnected with SteamID: {steamid}")
    print(connected_steamids)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    socketio.run(app, port=port, debug=True)
