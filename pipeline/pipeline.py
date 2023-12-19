"""
Pipeline script that connects the ETL scripts,
Runs the pipeline in a loop every 1 min.
"""

import time
from os import environ

from dotenv import load_dotenv

from extract import fetch_all_plant_data, convert_plant_data_to_csv
from transform import standardize_country_name, remove_rows_with_null, check_soil_moisture_valid, check_soil_temp_valid, normalize_datetimes, change_temp_and_moisture_to_two_dp
from load import create_database_connection, insert_into_recordings_table

if __name__ == "__main__":

    load_dotenv()

    while True:

        # Starts a timer for each iteration of the pipeline
        st = time.time()

        # Fetches all plant data from the api
        plant_api_data = fetch_all_plant_data()

        # Creates a csv file for the data and returns a data frame
        plants = convert_plant_data_to_csv(plant_api_data)

        # Location formatting
        plants["Country"] = plants["Country's Initials"].apply(
            standardize_country_name)

        # Drop redundant columns
        plants = plants.drop("Country's Initials", axis=1)

        # Drop rows with null values in important columns
        plants = remove_rows_with_null(plants, ["Id", "Name", "Recording Taken", "Soil Moisture",
                                                "Temperature", "Botanist Name", "Botanist Email", "Botanist Phone"])

        # Validate and round moisture and temperature values
        plants = check_soil_moisture_valid(plants)
        plants = check_soil_temp_valid(plants)
        plants = normalize_datetimes(plants)
        plants = change_temp_and_moisture_to_two_dp(plants)

        # Creates a connection to the SQL Server
        connection = create_database_connection(environ)

        # Inserts the current iterations data into the SQL Server
        insert_into_recordings_table(connection, plants)

        # get the end time
        et = time.time()

        # get the execution time
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')

        time.sleep(60)
