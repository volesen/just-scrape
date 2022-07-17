import json
import sqlite3
import xml.etree.ElementTree as ET

from typing import List, Set, Tuple
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

import api
import models


def scrape_all_restaurant_ids(coords: List[Tuple[float, float]]) -> Set[str]:
    # Fetch restaurant ids for all postal codes
    def scrape_restaurant_ids(coord):
        response = api.get_retaurants(coord)
        tree = ET.fromstring(response)
        return [id.text for id in tree.findall("./rt/id")]

    results = thread_map(scrape_restaurant_ids, coords)

    # Some restaurants belong to multiple postal codes
    # Get unique restaurant ids
    restaurant_ids = set()
    for ids in results:
        restaurant_ids.update(ids)

    return restaurant_ids


def scrape_all_restaurant_menus(restaurant_ids: Set[str]) -> List[models.Restaurant]:
    def scrape_restaurant_menu(restaurant_id):
        try:
            response = api.get_menu(restaurant_id)
            tree = ET.fromstring(response)
            restaurant = models.Restaurant.from_xml(tree)
            return restaurant
        except Exception:
            return None

    restaurants = thread_map(scrape_restaurant_menu, restaurant_ids)
    return [r for r in restaurants if r]


if __name__ == "__main__":
    with open("src/assets/postal_codes.json") as f:
        postal_codes = json.load(f)

    coordinates = [postal_code["visueltcenter"] for postal_code in postal_codes]

    tqdm.write("Scraping restaurant ids...")
    restaurant_ids = scrape_all_restaurant_ids(coordinates)

    tqdm.write("Scraping restaurant menus...")
    restaurants = scrape_all_restaurant_menus(restaurant_ids)

    tqdm.write("Writing to database...")

    conn = sqlite3.connect("data/restaurants.db")

    # Load table definitions
    with open("src/ddl/tables.sql") as f:
        conn.executescript(f.read())

    with conn.cursor() as cursor:
        for restaurant in restaurants:
            restaurant.insert_into_db(cursor)

    conn.commit()
