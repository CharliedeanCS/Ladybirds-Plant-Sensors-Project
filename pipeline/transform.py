from os import path
import pandas as pd
import country_converter as coco
import pycountry_convert as pc

EMAIL_RE = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
PHONE_RE = r""
DATE_RE = r""


def standardize_country_name(country_name: str) -> str:
    """
    Convert country code given into standard country name
    """
    return coco.convert(names=country_name, to='name_short')


def extract_continent(country_name):
    """
    Convert continent/city string given into standard continent name
    """
    result = country_name.split('/')

    return result[0]


def extract_city(continent_city_str: str) -> str:
    """
    Convert continent/city string given into standard city name
    """
    result = continent_city_str.split('/')

    return result[1]


def verify_email(phone_number: int) -> bool:
    """
    Check that phone numbers are of correct format
    """
    pass


def remove_rows_with_null(df, columns):
    """
    Remove rows with null values in specified columns of a DataFrame.
    """
    return df.dropna(subset=columns)


def check_soil_temperature_valid(soil_temp: float) -> bool:
    """
    Check if temperature reading is valid.
    """
    pass


def check_soil_moisture_valid(soil_moisture: float) -> bool:
    """
    Check if temperature reading is valid.
    """
    pass


if __name__ == "__main__":

    df = pd.read_csv("plant_data.csv")

    # Location formatting
    df["Country"] = df["Country's Initials"].apply(
        standardize_country_name)
    df["Continent"] = df["Continent/City"].apply(extract_continent)
    df["City"] = df["Continent/City"].apply(extract_city)

    # Drop redundant columns
    df = df.drop("Country's Initials", axis=1)
    df = df.drop('Continent/City', axis=1)

    # Drop null values in important columns
    df = remove_rows_with_null(df, ["Id", "Name", "Recording Taken", "Soil Moisture",
                               "Temperature", "Botanist Name", "Botanist Email", "Botanist Phone"])

    print(df.head())

    # check moisture and temperature
