import json

from coronapi.constants import DATA_FOLDER


def per_100k(quantity, population):
    return round(100000 * quantity / population, 2)


def per_million(quantity, population):
    return round(1000000 * quantity / population, 2)


def get_regional_template():
    with open("{}/regional_template.json".format(DATA_FOLDER), encoding="utf-8") as json_file:
        return json.load(json_file)


def get_communal_template():
    with open("{}/communal_template.json".format(DATA_FOLDER), encoding="utf-8") as json_file:
        return json.load(json_file)
