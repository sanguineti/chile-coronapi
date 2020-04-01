#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

from coronapi.constants import GOV_PAGE_URL

def scrapperGovPage(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html,"html.parser")

    container = page_soup.find("div", {"class":"contenido"})
    table = container.table.tbody
    rows = table.findAll("tr")

    index_data = 0
    dic = dict()

    for row in rows:
        index_data += 1
        if index_data > 3 and index_data < 20:
            dic[index_data-4] = {"region": row.findAll('td')[0].text,
                                 #TODO "regionInfo" : bla, cruzar datos con regional_template
                                 "new_cases": row.findAll('td')[1].text,
                                 "total_cases": row.findAll('td')[2].text,
                                 "percent_cases": row.findAll('td')[3].text,
                                 "deaths": row.findAll('td')[4].text}

    dicToJson = json.dumps(dic)
    return dicToJson

