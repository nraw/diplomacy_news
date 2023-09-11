import json
import re

import requests
from bs4 import BeautifulSoup


def get_backstabbr():
    res = requests.get(
        "https://www.backstabbr.com/game/KGB/5178831816753152/1903/spring"
    )
    res.text
    bs = BeautifulSoup(res.text, "lxml")
    orders = json.loads(re.search("var orders = (.*)", res.text)[1][:-1])
    units_by_player = json.loads(
        re.search("var unitsByPlayer = (.*)", res.text)[1][:-1]
    )
    territories = json.loads(re.search("var territories = (.*)", res.text)[1][:-1])
    return orders, units_by_player, territories
