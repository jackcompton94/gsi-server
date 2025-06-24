import requests
import glob

def test_live_snapshots():
    url = "http://10.0.0.76:8888/update_gsi"
    json_files = sorted(glob.glob("../snapshots/r3_live*.json"))
    # json_files = sorted(glob.glob("../snapshots/r1_freezetime0.json"))

    for json_file in json_files:
        with open(json_file, 'rb') as f:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=f
            )
        assert response.status_code == 200, f"Failed for {json_file}: {response.text}"
