import functools
from functools import wraps
from flask import request, jsonify
import jwt
from config import secret, response_messages
import time
import datetime
from bson.json_util import loads, dumps

def response(data = [], message = "success", success = True, total_count = 0, code = 0):
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

def token_control(f=None, roles=None):
    if not f:
        return functools.partial(token_control, roles=roles)
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = request.headers.get('token')

        if not token:
            return response(success = False, message = response_messages.token["not_found"], code = 403), 403

        try:
            data = jwt.decode(token, secret.authentication["SECRET_KEY"])
            current_time = time.mktime((datetime.datetime.now()).timetuple())

            if data["expiry_time"] > current_time:
                if data["role"] in roles:
                    return f(self, data)
                else:
                    return response(success = False, message = response_messages.token["authorization_error"], code = 401), 401
            else:
                return response(success = False, message = response_messages.token["token_expired"], code = 401), 401
        except:
            return response(data = [], success = False, message = response_messages.token["token_invalid"]), 401

        return f(*args, **kwargs)
    return decorated
