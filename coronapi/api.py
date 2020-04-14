from flask import Blueprint, jsonify, json, abort, request

from .constants import (
    NOT_FOUND_ERROR,
    V3_HISTORICAL_NATIONAL_PATH,
    V3_HISTORICAL_REGION_PATH,
    V3_HISTORICAL_COMMUNE_PATH,
    V3_LATEST_NATIONAL_PATH,
    V3_LATEST_REGIONAL_PATH,
    V3_LATEST_COMMUNES_PATH,
    V3_REGIONS,
    V3_COMMUNES,
)
from coronapi.helpers.get_data import (
    get_national_data,
    get_regional_data,
    get_communes_data,
    get_regional_template,
)


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# Historical endpoints
@bp.route(V3_HISTORICAL_NATIONAL_PATH, methods=["GET"])
def v3_historical_national():
    return json.dumps(get_national_data(), ensure_ascii=False)


@bp.route(V3_HISTORICAL_REGION_PATH, methods=["GET"])
def v3_historical_regions():
    data = get_regional_data()
    if "id" in request.args:
        id = int(request.args["id"])
        if id not in range(1, 17):
            return abort(404, description=NOT_FOUND_ERROR)
        return json.dumps(data[str(id)], ensure_ascii=False)

    return json.dumps(data, ensure_ascii=False)


@bp.route(V3_HISTORICAL_COMMUNE_PATH, methods=["GET"])
def v3_historical_communes():
    return json.dumps(get_communes_data(), ensure_ascii=False)


# latest endpoints
@bp.route(V3_LATEST_NATIONAL_PATH, methods=["GET"])
def v3_national_latest():
    data = get_national_data()
    max_key = max(data.keys())

    return json.dumps(data[max_key], ensure_ascii=False)


@bp.route(V3_LATEST_REGIONAL_PATH, methods=["GET"])
def v3_regional_latest():
    data = get_regional_data()
    for key in data:
        max_subkey = max(data[key]["regionData"].keys())
        data[key]["regionData"] = {max_subkey: data[key]["regionData"][max_subkey]}
    if "id" in request.args:
        id = int(request.args["id"])
        if id not in range(1, 17):
            return abort(404, description=NOT_FOUND_ERROR)
        return json.dumps(data[str(id)], ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


@bp.route(V3_LATEST_COMMUNES_PATH, methods=["GET"])
def v3_communes_latest():
    data = get_communes_data()

    for key in data:
        max_subkey = max(data[key]["confirmed"].keys())
        data[key]["confirmed"] = {max_subkey: data[key]["confirmed"][max_subkey]}
    if "id" in request.args:
        id = int(request.args["id"])

        try:
            return json.dumps(data[id], ensure_ascii=False)
        except KeyError:
            return abort(404, description=NOT_FOUND_ERROR)

    return json.dumps(data, ensure_ascii=False)


# Models endpoints
@bp.route(V3_REGIONS, methods=["GET"])
def v3_models_regions():
    data = get_regional_template()
    data_dict = dict()
    for key in data:
        data_dict.update({key: data[key]["region"]})
    return json.dumps(data_dict, ensure_ascii=False)


@bp.route(V3_COMMUNES, methods=["GET"])
def v3_models_communes():
    data = get_communes_data()
    data_dict = dict()
    for key in data:
        data_dict.update(
            {
                key: {
                    "commune": data[key]["commune"],
                    "region": data[key]["communeInfo"]["region"],
                }
            }
        )
    return json.dumps(data_dict, ensure_ascii=False)
