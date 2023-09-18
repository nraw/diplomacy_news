import json
import re

import requests
from bs4 import BeautifulSoup

from diplomacy_news.get_war_map import get_war_map


def get_backstabbr():
    base_url = "https://www.backstabbr.com"
    url = base_url + "/game/KGB/5178831816753152"
    res = requests.get(url)
    bs = BeautifulSoup(res.text, "lxml")
    stage = get_property("stage", res)
    if stage in ["SATISFIED", "NEEDS_BUILDS", "NEEDS_ORDERS"]:
        prev_season = bs.find("a", {"id": "history_previous_season"})["href"]
        url = base_url + prev_season
        res = requests.get(url)
        bs = BeautifulSoup(res.text, "lxml")
        get_war_map(url)

        #  stage = json.loads(re.search("var stage = (.*)", res.text)[1][:-1])
    season = bs.find("a", {"id": "history_current_season"})
    if season:
        season = season.text.strip().title()
    orders = get_property("orders", res)
    units_by_player = get_property("units_by_player", res)
    territories = get_property("territories", res)
    units_by_player = get_property("unitsByPlayer", res)
    orders = get_property("orders", res)
    return orders, units_by_player, territories, season


def get_property(property_name, res):
    pattern = f"var {property_name} = (.*)"
    match = re.search(pattern, res.text)
    if match:
        property_raw = match[1][:-1]
        property = json.loads(property_raw)
    else:
        property = ""
    return property
