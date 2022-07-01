from bson.json_util import loads, dumps
from config import secret

class ApiBase():
    def __init__(self):
        pass

    def response(self, data = [], message = "success", success = True, total_count = 0, code = 0):
        return {
            "data": {
                "data": dumps(data),
                "success": success,
                "message": message,
                "summary": {
                    "total_count": total_count,
                    "code": code
                }
            }
        }

    def request_validation(self, payload, required_keys):
        confirm = True
        missed_keys = ""

        for key in required_keys:
            if key not in payload or str(payload[key]).strip() == "":
                confirm = False
                missed_keys += f"{key}, "
        
        return missed_keys[:-2], confirm

    def check_request_params(self, payload, request_keys):
        params = {}

        for key in request_keys:
            if key in payload:
                params[key] = payload[key]

        return params