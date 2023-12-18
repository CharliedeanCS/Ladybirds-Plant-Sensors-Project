"""Extract script that pulls all plant data from the API."""
import os

import requests
import requests.exceptions
import pandas as pd

API_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def convert_plant_data_to_csv(plant_list: list[dict]) -> None:
    """Converts the list of all plant data into one csv file."""

    plant_dataframe = pd.DataFrame(plant_list)

    if not os.path.isfile('./data/plant_data.csv'):
        os.makedirs('./data/', exist_ok=True)
        plant_dataframe.to_csv('./data/plant_data.csv', header='column_names')
    else:  # else it exists so append without writing the header
        plant_dataframe.to_csv(
            './data/plant_data.csv', mode='a', header=False)

    return plant_dataframe


def flatten_and_organize_data(plant_dict: dict) -> dict:
    """Flattens the data and selects only the parts of the data we need."""

    if plant_dict == {}:
        raise ValueError("Plant data was empty")

    plant_id = str(int(plant_dict["plant_id"] + 1))

    botanist_email = plant_dict["botanist"]["email"]
    botanist_name = plant_dict["botanist"]["name"]
    botanist_phone = plant_dict["botanist"]["phone"]

    country_initials = plant_dict["origin_location"][3]
    continent = plant_dict["origin_location"][4].split("/")[0]
    region = plant_dict["origin_location"][2]

    new_plant_dict = {
        "Id": plant_id, "Name": plant_dict["name"], "Last Watered": plant_dict["last_watered"],
        "Recording Taken": plant_dict["recording_taken"],
        "Soil Moisture": plant_dict["soil_moisture"],
        "Temperature": plant_dict["temperature"], "Botanist Name": botanist_name,
        "Botanist Email": botanist_email,
        "Botanist Phone": botanist_phone, "Region": region, "Country's Initials": country_initials,
        "Continent": continent}

    return new_plant_dict


def fetch_all_plant_data() -> list[dict]:
    """
    Fetches all 50 plants data from the API,
    reads the data into a dict.
    """

    while_plants = True
    current_plant = 0
    all_plant_data = []

    try:
        while while_plants:
            response = requests.get(f"{API_URL}{current_plant}", timeout=10)
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

    convert_plant_data_to_csv(plant_data)
