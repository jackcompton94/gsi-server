import json
import logging
from flask import Flask, request
from data.game_data_extract import extract_data
from src.phase import handle_phase

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)


@app.route('/', methods=['POST'])
def handle_game_state_update():
    try:
        data = request.data.decode('UTF-8')
        json_data = json.loads(data)

        # Extract data from JSON
        game_data = extract_data(json_data)

        # Handle suggestion flow
        handle_phase(game_data)

        return 'OK', 200
    except Exception as e:
        print(f"Error processing game state update: {e}")
        return 'Error', 500


if __name__ == '__main__':
    app.run(port=8888)
