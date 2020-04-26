from flask import Blueprint, jsonify, json, abort, request

from .constants import (
    NOT_FOUND_REGION_ERROR,
    NOT_FOUND_COMMUNE_ERROR,
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
    return jsonify(get_national_data())


@bp.route(V3_HISTORICAL_REGION_PATH, methods=["GET"])
def v3_historical_regions():
    data = get_regional_data()
    if "id" in request.args:
        id = int(request.args["id"])
        if id not in range(1, 17):
            return abort(404, description=NOT_FOUND_REGION_ERROR)
        return jsonify(data[str(id)])

    return jsonify(data)


@bp.route(V3_HISTORICAL_COMMUNE_PATH, methods=["GET"])
def v3_historical_communes():
    data = get_communes_data()
    if "id" in request.args:
        id = int(request.args["id"])
        try:
            return jsonify(data[id])
        except KeyError:
            return abort(404, description=NOT_FOUND_COMMUNE_ERROR)

    return jsonify(get_communes_data())


# latest endpoints
@bp.route(V3_LATEST_NATIONAL_PATH, methods=["GET"])
def v3_national_latest():
    data = get_national_data()
    max_key = max(data.keys())

    return jsonify(data[max_key])


@bp.route(V3_LATEST_REGIONAL_PATH, methods=["GET"])
def v3_regional_latest():
    data = get_regional_data()
    for key in data:
        max_subkey = max(data[key]["regionData"].keys())
        data[key]["regionData"] = {max_subkey: data[key]["regionData"][max_subkey]}
    if "id" in request.args:
        id = int(request.args["id"])
        if id not in range(1, 17):
            return abort(404, description=NOT_FOUND_REGION_ERROR)
        return jsonify(data[str(id)])
    return jsonify(data)


@bp.route(V3_LATEST_COMMUNES_PATH, methods=["GET"])
def v3_communes_latest():
    data = get_communes_data()

    for key in data:
        max_subkey = max(data[key]["confirmed"].keys())
        data[key]["confirmed"] = {max_subkey: data[key]["confirmed"][max_subkey]}
    if "id" in request.args:
        id = int(request.args["id"])

        try:
            return jsonify(data[id])
        except KeyError:
            return abort(404, description=NOT_FOUND_COMMUNE_ERROR)

    return jsonify(data)


# Models endpoints
@bp.route(V3_REGIONS, methods=["GET"])
def v3_models_regions():
    data = get_regional_template()
    data_dict = dict()
    for key in data:
        data_dict.update(
            {
                key: {"region": data[key]["region"]}
            }
        )
        for attr, val in data[key]["regionInfo"].items():
            if attr in ["population", "area", "lat", "long"]:
                data_dict[key][attr] = val
    return jsonify(data_dict)


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
        for attr, val in data[key]["communeInfo"].items():
            if attr in ["population", "area", "hdi"]:
                data_dict[key][attr] = val 
    return jsonify(data_dict)
