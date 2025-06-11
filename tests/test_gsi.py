from utils.parsing import parse_gsi_payload

def test_parse_sample_payload():
    with open("tests/fixtures/live_train.json") as f:
        payload = parse_gsi_payload(f.read())

    assert payload.map.name == "de_train"
    assert payload.round.phase == "live"
