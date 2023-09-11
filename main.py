import re
from collections import defaultdict
from pathlib import Path
from diplomacy_news.get_backstabbr import get_backstabbr

countries = ["Austria", "England", "France", "Germany", "Italy", "Russia", "Turkey"]

def main():
    orders, units_by_player, territories = get_backstabbr()
    battles = get_battles(orders, territories)

def get_battles(orders, territories):
    all_regions = get_all_regions(orders)
    battles = check_battles(all_regions, orders, territories)
    battles_orders = get_battles_orders(battles, orders)
    battle_possessions = get_battles_possessions(battles, territories)
    summaries = get_summaries(battles, battles_orders, battles_possessions)


def get_all_regions(orders):
    all_regions = []
    for country, country_orders in orders.items():
        for source, order in country_orders.items():
            involved_regions = get_involved_regions(source, order)
            all_regions += involved_regions
    all_regions = list(set(all_regions))
    return all_regions

def check_battles(all_regions, orders, territories):
    unprocessed_regions = set(all_regions.copy())
    battles = []
    while unprocessed_regions:
        processed_region = unprocessed_regions.pop()

        unchecked_regions = {processed_region}
        checked_regions = set()
        while unchecked_regions:
            unchecked_region = unchecked_regions.pop()
            connected_regions = find_all_connected_regions(unchecked_region, orders, territories)
            new_regions = connected_regions - checked_regions - set([unchecked_region])
            unchecked_regions = unchecked_regions.union(new_regions)
            checked_regions = checked_regions.union(set([unchecked_region]))
        battles += [checked_regions]
        unprocessed_regions = unprocessed_regions - checked_regions
    battles.sort(key = lambda x: -len(x))
    return battles


def find_all_connected_regions(unchecked_region, orders, territories):
    connected_regions = []
    for country, country_orders in orders.items():
        for source, order in country_orders.items():
            involved_regions = get_involved_regions(source, order)
            if unchecked_region in involved_regions:
                connected_regions += involved_regions
    connected_regions = set(connected_regions)
    return connected_regions
    

def get_involved_regions(source, order):
    involved_regions = [source]
    if "from" in order:
        involved_regions += [order['from']]
    if "to" in order:
        involved_regions += [order['to']]
    return involved_regions

def get_battles_orders(battles, orders):
    battles_orders = []
    for battle in battles:
        battle_orders = get_battle_orders(battle, orders)
        battles_orders += [battle_orders]
    return battles_orders 

def get_battle_orders(battle, orders):
    battle_orders = []
    for region in battle:
        for country, country_orders in orders.items():
            for source, order in country_orders.items():
                involved_regions = get_involved_regions(source, order)
                if region in involved_regions:
                    order['origin'] = source
                    order['country'] = country
                    battle_orders += [order]

    battle_orders = list({v['origin']:v for v in battle_orders}.values())  # make unique
    return battle_orders


def get_battles_possessions(battles, territories):
    battles_possessions = []
    for battle in battles:
        battle_possessions = get_battle_possessions(battle, territories)
        battles_possessions += [battle_possessions]
    return battles_possessions 

def get_battle_possessions(battle, territories):
    battle_possessions = []
    for region in battle:
        if region in territories:
            possession = {"type": "OCCUPIED", "country": territories[region], "origin": region}
            battle_possessions += [possession]
    return battle_possessions

def get_summaries(battles, battles_orders, battles_possessions):
    for battle, battle_orders, battle_possessions in zip(battles, battles_orders, battles_possessions):
        countries_involved = get_countries_involved(battle_orders, battle_possessions)



    return summaries 

def get_countries_involved(battle_orders, battle_possessions):
    countries_ordering = {order['country'] for order in battle_orders}
    countries_possessing = {possession['country'] for possession in battle_possessions}
    countries_involved = countries_ordering.union(countries_possessing)
    return countries_involved 

