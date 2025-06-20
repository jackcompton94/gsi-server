import os
import json
from flask import Flask, request, jsonify
from utils.parser import parse_gsi_payload
from handlers.phase_handler import handle_phase_change
from utils.raw_display import display_gsi_data

app = Flask(__name__)

@app.route('/update_gsi', methods=['POST'])
def update_gsi():
    try:
        data = request.data.decode('UTF-8')
        # json_data = json.loads(data)
        # display_gsi_data(json_data)

        payload = parse_gsi_payload(data)
        handle_phase_change(payload)

        return 'OK', 200
    except Exception as e:
        print(f"Error processing GSI update: {e}")
        return 'Error', 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'GSI Server is running'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port, debug=True)
