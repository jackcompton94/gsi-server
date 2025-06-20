import json
from dacite import from_dict
from models.gsi import GSIPayload

def parse_gsi_payload(json_data: str) -> GSIPayload:
    data = json.loads(json_data)
    return from_dict(data_class=GSIPayload, data=data)
