from flask import Flask, jsonify, request, Response
from flask_classful import FlaskView, route
from middlewares.ApiBase import ApiBase
from config import required_keys, request_keys, response_messages, secret
from helpers.HelperFunctions import token_control
import dtweb

class TwinbaseController(FlaskView, ApiBase):
    @route("getDTByID", methods = ["POST"])
    def getDTByID(self):
        try:
            missed_keys, confirm = ApiBase.request_validation(self, request.json, required_keys.twinbase["getDTByID"])

            if not confirm:
                return ApiBase.response(self, message = f"{missed_keys} {response_messages.general['payload_empty']}"), 400

            dt_doc = dtweb.client.fetch_dt_doc(request.json["dt-id"])

            return ApiBase.response(self, data = dt_doc, message = "Test"), 200
        except:
            return ApiBase.response(self, message = response_messages.general["unexpected_error"]), 400
