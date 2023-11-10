from flask import Blueprint

api = Blueprint("api", __name__)


@api.route("/v2/ping")
def ping():
    return "pong"
