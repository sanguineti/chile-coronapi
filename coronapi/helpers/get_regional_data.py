import requests
import json
import csv
import os
import io

from coronapi.constants import REGIONAL_URL

DATAWRAPPER_TOKEN = os.getenv("DATAWRAPPER_TOKEN")
headers = {
    "Authorization": "Bearer {}".format(DATAWRAPPER_TOKEN),
}


def get_regional_data():
    response = requests.request("GET", REGIONAL_URL, headers=headers)

    with open("coronapi/data/regional_template.json") as json_file:
        data = json.load(json_file)
    parsed_response = io.StringIO(response.content.decode("utf-8"))
    csv_reader = csv.DictReader(parsed_response, delimiter=";")
    for row in csv_reader:
        data[str(csv_reader.line_num - 1)]["confirmed"] = row["contagios"]

    return list(data.values())
