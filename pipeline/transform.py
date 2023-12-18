from os import path
import pandas as pd
import country_converter as coco


def standardize_country_name(country_name: str) -> str:
    """
    Convert country code given into standard country name
    """
    return coco.convert(names=country_name, to='name_short')


def remove_rows_with_null(df, columns):
    """
    Remove rows with null values in specified columns of a DataFrame.
    """
    return df.dropna(subset=columns)


def check_soil_temp_valid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check if temperature reading is valid.
    """
    temp_conditions = (
        (df['Temperature'] > 0) &
        (df['Temperature'] < 30)
    )

    return df[temp_conditions]


def check_soil_moisture_valid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check if temperature reading is valid.
    """
    moisture_conditions = (
        (df['Soil Moisture'] > 0) &
        (df['Soil Moisture'] < 100)
    )

    return df[moisture_conditions]


def normalize_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check if datetimes are valid. Drop non-valid values
    """
    df['Last Watered'] = pd.to_datetime(df['Last Watered'])
    df['Recording Taken'] = pd.to_datetime(df['Recording Taken'])

    return df


if __name__ == "__main__":

    df = pd.read_csv("plant_data.csv")

    # Location formatting
    df["Country"] = df["Country's Initials"].apply(
        standardize_country_name)

    # Drop redundant columns
    df = df.drop("Country's Initials", axis=1)

    # Drop null values in important columns
    df = remove_rows_with_null(df, ["Id", "Name", "Recording Taken", "Soil Moisture",
                               "Temperature", "Botanist Name", "Botanist Email", "Botanist Phone"])

    # check moisture and temperature
    df = check_soil_moisture_valid(df)
    df = check_soil_temp_valid(df)
    df = normalize_datetimes(df)

    #  Add clean data to new file
    df.to_csv(('cleaned_plant_data.csv'), index=False)
