import requests
import csv
import io
import copy

from coronapi.constants import (
    REGIONAL_CONFIRMED_URL,
    REGIONAL_DEATHS_URL,
    NATIONAL_URL,
    COMMUNES_URL,
    INE_CHILEAN_HABITANTS,
)
from coronapi.helpers.utils import (
    per_100k,
    get_regional_template,
    get_communal_template,
    per_million
)


def get_regional_data():
    data = get_regional_template()
    confirmed_response = requests.request("GET", REGIONAL_CONFIRMED_URL)
    deaths_response = requests.request("GET", REGIONAL_DEATHS_URL)
    parsed_confirmed_response = io.StringIO(confirmed_response.content.decode("utf-8"))
    parsed_deaths_response = io.StringIO(deaths_response.content.decode("utf-8"))
    confirmed_reader = csv.DictReader(parsed_confirmed_response, delimiter=",")
    deaths_reader = csv.DictReader(parsed_deaths_response, delimiter=",")

    for confirmed_row, deaths_row in zip(confirmed_reader, deaths_reader):
        region_id = confirmed_row["codigo"]
        del confirmed_row["codigo"], confirmed_row["region"]
        del deaths_row["codigo"], deaths_row["region"]
        population = data[region_id]["regionInfo"]["population"]
        region_data = dict()

        for key in confirmed_row:
            confirmed = int(confirmed_row[key])
            region_data.update(
                {
                    key: {
                        "confirmed": confirmed,
                        "confirmed_per_100k": per_100k(confirmed, population),
                        "confirmed_per_million": per_million(confirmed, population),
                    }
                }
            )

        for key in deaths_row:
            deaths = int(deaths_row[key])
            region_data[key].update(
                {
                    "deaths": deaths,
                    "deaths_per_100k": per_100k(deaths, population),
                    "deaths_per_million": per_million(deaths, population),
                }
            )

        data[region_id]["regionData"] = region_data
    return data


def get_national_data():
    response = requests.request("GET", NATIONAL_URL)
    parsed_response = io.StringIO(response.content.decode("utf-8"))
    data = csv.DictReader(parsed_response, delimiter=",")
    data_dict = dict()
    for element in data:
        element["confirmed"] = int(element.pop("confirmados"))
        element["day"] = element.pop("dia")
        element["deaths"] = int(element.pop("muertes"))
        element["confirmed_per_100k"] = per_100k(
            int(element["confirmed"]), INE_CHILEAN_HABITANTS
        )
        element["confirmed_per_million"] = per_million(
            int(element["confirmed"]), INE_CHILEAN_HABITANTS
        )
        element["deaths_per_100k"] = per_100k(
            int(element["deaths"]), INE_CHILEAN_HABITANTS
        )
        element["deaths_per_million"] = per_million(
            int(element["deaths"]), INE_CHILEAN_HABITANTS
        )
        data_dict.update({element["day"]: element})
    return data_dict

#TODO eliminar el confirmed al pasar a v4 y deprecar v3

def get_communes_data():
    response = requests.request("GET", COMMUNES_URL)
    parsed_response = io.StringIO(response.content.decode("utf-8"))
    data = list(csv.DictReader(parsed_response, delimiter=","))
    dict_data = dict()
    data_communes = get_communal_template()

    for element in data:
        commune_info = {
            "region": element.pop("region"),
            "region_code": int(element.pop("codigo_region")),
            "_id": int(element.pop("codigo_comuna")),
        }
        for key, val in data_communes[str(commune_info["_id"])].items():
            commune_info[key] = val
            if key == "hdi":
                commune_info[key] = round(val, 3)
        commune = element.pop("comuna")
        confirmed_per_commune = copy.deepcopy(element)

        commune_data = dict()

        for key in confirmed_per_commune:
            if confirmed_per_commune[key] == "-":
                commune_data[key] = {
                    "confirmed": 0,
                }
                confirmed_per_commune[key] = 0
            else:
                commune_data[key] = {
                    "confirmed": int(confirmed_per_commune[key].replace(",", "").replace(".", "")),
                }
                confirmed_per_commune[key] = int(confirmed_per_commune[key].replace(",", "").replace(".", ""))

        dict_data.update(
            {
                commune_info["_id"]: {
                    "communeInfo": commune_info,
                    "commune": commune,
                    "confirmed": confirmed_per_commune,
                    "communeData": commune_data,
                }
            }
        )

    return dict_data


def get_commune_by_all_regions():
    response = requests.request("GET", COMMUNES_URL)
    parsed_response = io.StringIO(response.content.decode("utf-8"))
    data = list(csv.DictReader(parsed_response, delimiter=","))
    dict_data = dict()
    for i in range(1, 17):
        dict_data[i] = dict()
    data_communes = get_communal_template()
    for element in data:
        id_region = int(element.pop("codigo_region"))
        commune_info = {
            "region": element.pop("region"),
            "region_code": id_region,
            "_id": int(element.pop("codigo_comuna")),
        }
        for key, val in data_communes[str(commune_info["_id"])].items():
            commune_info[key] = val
            if key == "hdi":
                commune_info[key] = round(val, 3)
        commune = element.pop("comuna")
        confirmed_per_commune = copy.deepcopy(element)

        commune_data = dict()

        for key in confirmed_per_commune:
            if confirmed_per_commune[key] == "-":
                commune_data[key] = {
                    "confirmed": 0,
                }
            else:
                commune_data[key] = {
                    "confirmed": int(confirmed_per_commune[key].replace(",", "").replace(".", "")),
                }

        dict_data[id_region].update(
            {
                commune_info["_id"]: {
                    "communeInfo": commune_info,
                    "commune": commune,
                    "communeData": commune_data,
                }
            }
        )

    return dict_data
