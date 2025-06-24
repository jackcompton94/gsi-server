import json
import logging
import os
import threading

from flask import Flask, request
from ui.log_terminal import start_terminal
from utils.parser import parse_gsi_payload
from handlers.phase_handler import process_game_state
from utils.raw_display import display_gsi_data

app = Flask(__name__)

@app.route('/update_gsi', methods=['POST'])
def receive_game_state_integration_update():
    """Handles incoming CS2 Game State Integration (GSI) webhook requests.
    
    This endpoint receives real-time game data from CS2 and processes it
    to provide AI coaching insights and track game events.
    """
    try:
        data = request.data.decode('UTF-8')
        payload = parse_gsi_payload(data)
        # display_gsi_data(payload.__dict__)
        process_game_state(payload)
        return 'OK', 200
    except Exception as e:
        logging.error(f"Error processing GSI update: {e}")
        return 'Error', 500


def start_flask_server():
    """Initializes and starts the Flask web server for CS2 GSI webhook reception.
    
    Configures the server to listen on all interfaces (0.0.0.0) on the specified port.
    """
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    start_terminal()