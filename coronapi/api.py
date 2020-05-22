from flask import Blueprint, jsonify, json, abort, request, Response
from flask_cors import CORS

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
    V3_LATEST_COMMUNES_BY_REGION_PATH,
V3_HISTORICAL_COMMUNES_BY_REGION_PATH,
)
from coronapi.helpers.get_data import (
    get_national_data,
    get_regional_data,
    get_communes_data,
    get_regional_template,
    get_communes_by_region_data,
    get_commune_by_all_regions,
)


bp = Blueprint("api", __name__, url_prefix="/api")
CORS(bp)


@bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# Historical endpoints
@bp.route(V3_HISTORICAL_NATIONAL_PATH, methods=["GET"])
def v3_historical_national():
    return Response(
        json.dumps(get_national_data(), ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


@bp.route(V3_HISTORICAL_REGION_PATH, methods=["GET"])
def v3_historical_regions():
    data = get_regional_data()
    if "id" in request.args:
        id = int(request.args["id"])
        if id not in range(1, 17):
            return abort(404, description=NOT_FOUND_REGION_ERROR)
        return Response(
            json.dumps(data[str(id)], ensure_ascii=False),
            content_type="application/json; charset=utf-8",
        )

    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


@bp.route(V3_HISTORICAL_COMMUNE_PATH, methods=["GET"])
def v3_historical_communes():
    data = get_communes_data()
    if "id" in request.args:
        id = int(request.args["id"])
        try:
            return Response(
                json.dumps(data[id], ensure_ascii=False),
                content_type="application/json; charset=utf-8",
            )
        except KeyError:
            return abort(404, description=NOT_FOUND_COMMUNE_ERROR)

    return Response(
        json.dumps(get_communes_data(), ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


# latest endpoints
@bp.route(V3_LATEST_NATIONAL_PATH, methods=["GET"])
def v3_national_latest():
    data = get_national_data()
    max_key = max(data.keys())

    return Response(
        json.dumps(data[max_key], ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


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
        return Response(
            json.dumps(data[str(id)], ensure_ascii=False),
            content_type="application/json; charset=utf-8",
        )

    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


@bp.route(V3_LATEST_COMMUNES_PATH, methods=["GET"])
def v3_communes_latest():
    data = get_communes_data()

    for key in data:
        max_subkey = max(data[key]["confirmed"].keys())
        data[key]["confirmed"] = {max_subkey: data[key]["confirmed"][max_subkey]}
    if "id" in request.args:
        id = int(request.args["id"])

        try:
            return Response(
                json.dumps(data[id], ensure_ascii=False),
                content_type="application/json; charset=utf-8",
            )
        except KeyError:
            return abort(404, description=NOT_FOUND_COMMUNE_ERROR)

    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


# Models endpoints
@bp.route(V3_REGIONS, methods=["GET"])
def v3_models_regions():
    data = get_regional_template()
    data_dict = dict()
    for key in data:
        data_dict.update({key: {"region": data[key]["region"]}})
        for attr, val in data[key]["regionInfo"].items():
            if attr in ["_id", "population", "area", "lat", "long", "hdi"]:
                data_dict[key][attr] = val
    return Response(
        json.dumps(data_dict, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


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
            if attr in ["_id", "population", "area", "hdi"]:
                data_dict[key][attr] = val
    return Response(
        json.dumps(data_dict, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


@bp.route(V3_LATEST_COMMUNES_BY_REGION_PATH, methods=["GET"])
def v3_communes_by_region_latest():
    if "region_id" in request.args:
        id = int(request.args["region_id"])

        data = get_communes_by_region_data(id)

        for key in data:
            max_subkey = max(data[key]["confirmed"].keys())
            data[key]["confirmed"] = {max_subkey: data[key]["confirmed"][max_subkey]}
        try:
            return Response(
                json.dumps(data, ensure_ascii=False),
                content_type="application/json; charset=utf-8",
            )
        except KeyError:
            return abort(404, description=NOT_FOUND_REGION_ERROR)
    else:
        data = get_commune_by_all_regions()
        for region in data:
            for key in data[region]:
                max_subkey = max(data[region][key]["confirmed"].keys())
                data[region][key]["confirmed"] = {max_subkey: data[region][key]["confirmed"][max_subkey]}
        return Response(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json; charset=utf-8",
        )

@bp.route(V3_HISTORICAL_COMMUNES_BY_REGION_PATH, methods=["GET"])
def v3_communes_by_region_historical():
    if "region_id" in request.args:
        id = int(request.args["region_id"])

        data = get_communes_by_region_data(id)


        try:
            return Response(
                json.dumps(data, ensure_ascii=False),
                content_type="application/json; charset=utf-8",
            )
        except KeyError:
            return abort(404, description=NOT_FOUND_REGION_ERROR)
    else:
        data = get_commune_by_all_regions()
        return Response(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json; charset=utf-8",
        )