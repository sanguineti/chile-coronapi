import requests
import json
import csv
import os

from coronapi.constants import REGIONAL_URL

DATAWRAPPER_TOKEN = os.getenv("DATAWRAPPER_TOKEN")
headers = {
    "Authorization": "Bearer {}".format(DATAWRAPPER_TOKEN),
}


def get_regional_data():
    response = requests.request("GET", REGIONAL_URL, headers=headers)

    with open("coronapi/data/regional_temp.csv", "wb") as out_file:
        out_file.write(response.content)

    with open("coronapi/data/regional_template.json") as json_file:
        data = json.load(json_file)

    with open("coronapi/data/regional_temp.csv") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for row in csv_reader:
            data[str(csv_reader.line_num - 1)]["confirmed"] = row["contagios"]

    with open("coronapi/data/regional.json", "w", encoding="utf8") as jfile:
        json.dump(list(data.values()), jfile, ensure_ascii=False)

    os.remove("coronapi/data/regional_temp.csv")
