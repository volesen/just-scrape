import json
import sqlite3

from typing import List, Set, Tuple
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET

import api
import models


def scrape_all_restaurant_ids(coords: List[Tuple[float, float]]) -> Set[str]:
    # Fetch restaurant ids for all postal codes
    def scrape_restaurant_ids(coord):
        response = api.get_retaurants(*coord)
        tree = ET.fromstring(response)

        return [id.text for id in tree.findall("./rt/id")]

    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_restaurant_ids, coords)

    # Some restaurants belong to multiple postal codes
    restaurant_ids = set()
    for ids in results:
        restaurant_ids.update(ids)

    return restaurant_ids


def scrape_all_restaurant_menus(
    cursor, restaurant_ids: Set[str]
) -> List[models.Restaurant]:
    def scrape_restaurant_menu(restaurant_id):
        try:
            response = api.get_menu(restaurant_id)
            tree = ET.fromstring(response)
            restaurant = models.Restaurant.from_xml(tree)
            return restaurant
        except Exception:
            return None

    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_restaurant_menu, restaurant_ids)
        for result in results:
            if result is not None:
                result.insert_into_db(cursor)


if __name__ == "__main__":
    # Step 1: Fetch all restaurant ids
    with open("src/assets/postal_codes.json") as f:
        postal_codes = json.load(f)

    coordinates = [
        reversed(postal_code["visueltcenter"]) for postal_code in postal_codes
    ]

    restaurant_ids = scrape_all_restaurant_ids(coordinates)

    # Step 2: Fetch all restaurant menus and insert into db

    with sqlite3.connect("restaurants.db") as conn:
        cursor = conn.cursor()

        # Create tables from "models.sql" file
        with open("src/ddl/tables.sql") as f:
            cursor.executescript(f.read())

        scrape_all_restaurant_menus(cursor, restaurant_ids)

        cursor.close()
        conn.commit()
