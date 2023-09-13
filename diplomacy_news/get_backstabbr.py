import json
import re

import requests
from bs4 import BeautifulSoup


def get_backstabbr():
    res = requests.get("https://www.backstabbr.com/game/KGB/5178831816753152")
    bs = BeautifulSoup(res.text, "lxml")
    stage = json.loads(re.search("var stage = (.*)", res.text)[1][:-1])
    if stage in ["SATISFIED", "NEEDS_BUILDS"]:
        prev_season = bs.find("a", {"id": "history_previous_season"})["href"]
        res = requests.get("https://www.backstabbr.com" + prev_season)
        bs = BeautifulSoup(res.text, "lxml")
        #  stage = json.loads(re.search("var stage = (.*)", res.text)[1][:-1])
    season = bs.find("a", {"id": "history_current_season"})
    if season:
        season = season.text.strip().title()
    orders = json.loads(re.search("var orders = (.*)", res.text)[1][:-1])
    units_by_player = json.loads(
        re.search("var unitsByPlayer = (.*)", res.text)[1][:-1]
    )
    territories = json.loads(re.search("var territories = (.*)", res.text)[1][:-1])
    return orders, units_by_player, territories, season
