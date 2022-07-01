from flask import Flask, jsonify, request, Response
from flask_classful import FlaskView, route
from middlewares.ApiBase import ApiBase
from helpers.HelperFunctions import token_control
from flask_cors import CORS

from controllers.TwinbaseController import TwinbaseController


class Api(FlaskView, ApiBase):
    @route("test", methods = ["POST"])
    @token_control(roles = ["admin", "user"])
    def test(self, user):
        return ApiBase.response(self, data = ["one", "two"], message = "response msg", success = True)


if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    Api.register(app, route_base = '/api/')
    TwinbaseController.register(app, route_base = '/api/twinbase/')
    app.run(debug = True, port = 5001)