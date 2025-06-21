import logging
import os
import threading
from flask import Flask, request

from ui.log_terminal import start_terminal
from utils.parser import parse_gsi_payload
from handlers.phase_handler import handle_phase_change
from ui import log_terminal

app = Flask(__name__)

@app.route('/update_gsi', methods=['POST'])
def update_gsi():
    try:
        data = request.data.decode('UTF-8')
        payload = parse_gsi_payload(data)
        handle_phase_change(payload)
        return 'OK', 200
    except Exception as e:
        logging.error(f"Error processing GSI update: {e}")
        return 'Error', 500


def run_flask():
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    start_terminal()