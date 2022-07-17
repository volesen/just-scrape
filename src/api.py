import hashlib
import requests
from typing import Tuple

LANG = "da"  # or "en"
DELIVERY_AREA_ID = ""  # Not quite sure what this is. Reversed engineered from the app.
COUNTRY_CODE = "7"  # Denmark
IS_ADDRESS_ACCURATE = "1"  # Either 0 or 1
PASSWORD = "4ndro1d"  # Used in hash


def get_retaurants(coord: Tuple[float, float]) -> str:
    """
    Get the list of restaurants for a given coordinate.
    """
    lng, lat = coord

    to_hash = f"getrestaurants{DELIVERY_AREA_ID}{COUNTRY_CODE}{lat:.7f}{lng:.7f}{LANG}0{IS_ADDRESS_ACCURATE}{PASSWORD}"
    hash = hashlib.md5(to_hash.encode()).hexdigest()

    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "okhttp/3.14.7",
    }

    data = {
        "var0": hash,
        "var1": "getrestaurants",
        "var2": DELIVERY_AREA_ID,
        "var3": COUNTRY_CODE,
        "var4": f"{lat:.7f}",
        "var5": f"{lng:.7f}",
        "var6": LANG,
        "var7": "0",  # Always zero for getrestaurants
        "var8": IS_ADDRESS_ACCURATE,
        "version": "5.32",
        "systemversion": "28;8.0.28.0.2",
        "appname": "just-eat.dk",
        "language": "en",
    }

    response = requests.post(
        "https://dk.citymeal.com/android/android.php/", headers=headers, data=data
    )

    return response.text


def get_menu(restaurant_id: str) -> str:
    """
    Get the menu for a given restaurant.
    """

    headers = {
        "platform": "android",
        "appname": "just-eat.dk",
        "appversion": "8.0.2",
        "systemversion": "28;8.0.2",
        "user-agent": "okhttp/3.14.7",
    }

    response = requests.get(
        f"https://dk-cdn.citymeal.com/ws/6.0.8/getrestaurantdata/{restaurant_id}/{LANG}",
        headers=headers,
    )

    return response.text
