import json
import os

from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup

from coronapi.constants import CHILEAN_FLAG, GOV_PAGE_URL
from .utils import get_per_one_million, undotter


def format_date_last_update(date_string):
    date_str = date_string.replace("*Informe corresponde al ", "").replace(".", "")
    months = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    name_month = date_str.split()[2].lower()
    day = "{:0>2d}".format(int(date_str.split()[0]))
    number_month = "{:0>2d}".format(months.index(name_month) + 1)
    year = date_str.split()[4]

    return "{}/{}/{}".format(day, number_month, year)


def get_regions_info():
    data_folder = os.path.join("coronapi", "data")
    file = os.path.join(data_folder, "regional_template.json")
    regions = []

    with open(file) as json_file:
        data = json.load(json_file)
        for key in data:
            data_region = data[key]
            region = {
                "region": data_region["region"],
                "regionInfo": data_region["regionInfo"],
            }
            regions.append(region)

    return json.dumps(regions, ensure_ascii=False)


def get_gov_page():
    uclient = ureq(GOV_PAGE_URL)
    page_html = uclient.read()
    uclient.close()
    page_soup = soup(page_html, "html.parser")
    container = page_soup.find("div", {"class": "contenido"})
    table = container.table.tbody
    date = container.p.strong
    rows = table.findAll("tr")
    recovered = undotter(page_soup.find_all("table")[1].findAll("td")[1].text)

    return {"rows": rows, "date": date, "recovered": recovered}


def get_regional():
    regions_data = json.loads(get_regions_info())
    gov_data = get_gov_page()
    rows, date = map(gov_data.get, ("rows", "date"))

    index_data = 0
    dict_per_region = dict()
    region_info = {}

    for row in rows:
        index_data += 1
        if 3 < index_data < 20:
            for name_region in regions_data:
                if row.findAll("td")[0].text == name_region["region"]:
                    region_info = name_region["regionInfo"]
                dict_per_region[index_data - 4] = {
                    "region": row.findAll("td")[0].text,
                    "regionInfo": region_info,
                    "new_daily_cases": undotter(row.findAll("td")[1].text),
                    "confirmed": undotter(row.findAll("td")[2].text),
                    "deaths": undotter(row.findAll("td")[4].text),
                    "last_updated": format_date_last_update(date.text),
                }

    return dict_per_region


def get_national():
    gov_data = get_gov_page()
    rows, date, recovered = map(gov_data.get, ("rows", "date", "recovered"))
    daily_new_cases = undotter(rows[19].findAll("td")[1].text)
    confirmed = undotter(rows[19].findAll("td")[2].text)
    deaths = undotter(rows[19].findAll("td")[4].text)

    per_million = get_per_one_million(confirmed, deaths)

    return {
        "country": "Chile",
        "country_info": {
            "_id": 152,
            "iso2": "CL",
            "iso3": "CHL",
            "lat": -30,
            "long": -71,
            "flag": CHILEAN_FLAG,
        },
        "daily_new_cases": daily_new_cases,
        "confirmed": confirmed,
        "deaths": deaths,
        "last_updated": format_date_last_update(date.text),
        "recovered": recovered,
        "active": confirmed - recovered,
        "confirmed_per_one_million": per_million[0],
        "deaths_per_one_million": per_million[1],
    }
