import threading
import time
import requests
import glob

from ui.log_terminal import push_log, start_terminal


def test_live_snapshots():
    url = "http://10.0.0.76:8888/update_gsi"
    json_files = sorted(glob.glob("../snapshots/*.json"))

    for json_file in json_files:
        with open(json_file, 'rb') as f:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=f
            )
        assert response.status_code == 200, f"Failed for {json_file}: {response.text}"

def test_ui():
    # Start a thread to push some logs after the UI starts
    def feed_logs():
        logs = [
            "[INFO] Starting test UI...",
            "[STRATEGY] Execute fast push",
            "[ACTION] Throw flashbang",
            "[INFO] Waiting for next tick..."
        ]
        for line in logs:
            push_log(line)
            time.sleep(3)

    # Start feeding logs in background thread
    threading.Thread(target=feed_logs, daemon=True).start()

    # Start the UI (blocking call)
    start_terminal(skip_splash=True)
