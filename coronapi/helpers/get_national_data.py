import requests
import json
import csv
import os

from coronapi.constants import NATIONAL_URL

DATAWRAPPER_TOKEN = os.getenv("DATAWRAPPER_TOKEN")
headers = {
    "Authorization": "Bearer {}".format(DATAWRAPPER_TOKEN),
}


def date_format(date_string):
    months = {
        "mar": "/03/2020",
        "abr": "/04/2020",
        "may": "/05/2020",
        "jun": "/06/2020",
        "jul": "/07/2020",
    }
    x = date_string.split("-")

    return "{}{}".format(x[0], months[x[1]])


def get_national_data():
    response = requests.request("GET", NATIONAL_URL, headers=headers)

    with open("coronapi/data/national_temp.csv", "wb") as out_file:
        out_file.write(response.content)

    data = []
    with open("coronapi/data/national_temp.csv") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            data.append(
                {
                    "date": date_format(row["Fecha"]),
                    "confirmed": row["contagios"],
                    "last_day_confirmed": row["aumento"],
                }
            )

    with open("coronapi/data/national.json", "w", encoding="utf8") as jfile:
        json.dump(data, jfile, ensure_ascii=False)

    os.remove("coronapi/data/national_temp.csv")
