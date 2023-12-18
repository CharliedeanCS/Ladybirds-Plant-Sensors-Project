"""Extract script that pulls all plant data from the API."""
import csv

import requests
import requests.exceptions

API_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def fetch_all_plant_data() -> list[dict]:
    """
    Fetches all 50 plants data from the API,
    reads the data into a dict.
    """

    while_plants = True
    current_plant = 47
    all_plant_data = []

    try:
        while while_plants:
            response = requests.get(f"{API_URL}{current_plant}")
            plant_json = response.json()
            plant_keys = plant_json.keys()

            if 'error' not in plant_keys:
                new_plant = flatten_and_organize_data(plant_json)
                all_plant_data.append(new_plant)

            current_plant += 1
    except requests.exceptions.JSONDecodeError:
        while_plants = False

    return all_plant_data


if __name__ == "__main__":
    plant_data = fetch_all_plant_data()

    print(plant_data)
