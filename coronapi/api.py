import requests

from flask import Blueprint, jsonify, json, abort, request

from .constants import (
    NOT_FOUND_ERROR,
    REGIONAL_PATH,
    LATEST_NATIONAL_PATH,
    NOVEL_COVID_ENDPOINT,
    # HISTORICAL_NATIONAL_PATH,
)
from coronapi.helpers.get_regional_data import get_regional_data

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@bp.route(REGIONAL_PATH, methods=["GET"])
def regions():
    data = get_regional_data()
    if "id" in request.args:
        id = int(request.args["id"])
        if id not in range(1, 17):
            return abort(404, description=NOT_FOUND_ERROR,)
        for val in data:
            if val["regionInfo"]["_id"] == id:
                return json.dumps(val, ensure_ascii=False)

    return json.dumps(data, ensure_ascii=False)


@bp.route(LATEST_NATIONAL_PATH, methods=["GET"])
def national_latest():
    data = requests.request("GET", NOVEL_COVID_ENDPOINT)
    return json.loads(data.text)


# @bp.route(HISTORICAL_NATIONAL_PATH, methods=["GET"])
# def national_historical():
#     with open("coronapi/data/national.json") as json_file:
#         data = json.load(json_file)
#         return json.dumps(data, ensure_ascii=False)
