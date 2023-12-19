"""Script to connect to an MSSQL database and insert plant data"""


from os import environ, _Environ

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Connection
from sqlalchemy.exc import IntegrityError
import pandas as pd

from transform import csv_to_data_frame


def create_database_connection(config: _Environ) -> Connection:
    """Creates a database connection to the SQL Server"""

    engine = create_engine(
        f"mssql+pymssql://{config['DB_USERNAME']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/?charset=utf8")

    conn = engine.connect()

    return conn


def insert_into_location_table(connection: Connection, plant_data: pd.DataFrame) -> None:
    """Inserts data from a pandas data frame into a SQL Server into the location table"""

    plant_list = plant_data.values.tolist()

    for plant in plant_list:

        try:
            region = plant[9]
            continent = plant[10]
            country = plant[11]

            connection.execute(sql.text("USE plants;"))

            query = sql.text(
                """INSERT INTO s_delta.location (region,country,continent)
                VALUES (:region,:continent,:country)""")
            connection.execute(
                query, {"region": region, "continent": continent, "country": country})
        except IntegrityError:
            pass


def insert_into_botanist_table(connection: Connection, plant_data: pd.DataFrame) -> None:
    """Inserts data from a pandas data frame into a SQL Server into the location table"""

    plant_list = plant_data.values.tolist()

    for plant in plant_list:

        try:
            name = plant[6]
            email = plant[7]
            telephone = plant[8]

            connection.execute(sql.text("USE plants;"))

            query = sql.text(
                """INSERT INTO s_delta.botanist (name,email,telephone_number)
                VALUES (:name,:email,:telephone)""")
            connection.execute(
                query, {"name": name, "email": email, "telephone": telephone})
        except IntegrityError:
            pass


def insert_into_plant_table(conn: Connection, plant_data: list[dict]) -> None:
    """Seed the plant table with the plant data list and relevant botanist and location ids."""

    plant_data = plant_data.to_dict('records')

    for plant in plant_data:

        try:

            query = sql.text(
                "SELECT botanist_id FROM s_delta.botanist WHERE telephone_number = (:num)")
            args = ({"num": plant["Botanist Phone"]})
            botanist_id = conn.execute(query, args).fetchone()[0]

            query = sql.text(
                "SELECT location_id FROM s_delta.location WHERE region = (:region)")
            args = ({"region": plant["Region"]})
            location_id = conn.execute(query, args).fetchone()[0]

            query = sql.text(
                "INSERT INTO s_delta.plant (plant_id, name, botanist_id, location_id) VALUES (:id, :name, :b_id, :l_id)")
            args = ({"id": plant["Id"], "name": plant["Name"], "b_id": botanist_id,
                    "l_id": location_id})
            conn.execute(query, args)

        except IntegrityError:
            pass


def insert_into_recordings_table(connection: Connection, plant_data: pd.DataFrame) -> None:
    """Inserts data from a pandas data frame into a SQL Server into the recording table"""

    plant_list = plant_data.values.tolist()

    for plant in plant_list:

        query = sql.text(
            "SELECT plant_id FROM s_delta.plant WHERE name = (:name)")
        args = ({"name": plant[1]})
        id = connection.execute(query, args).fetchone()[0]

        soil = plant[4]
        temperature = plant[5]
        recording = plant[3]
        watered = plant[2]

        connection.execute(sql.text("USE plants;"))

        query = sql.text(
            """INSERT INTO s_delta.recording (plant_id,soil_moisture,temperature,recording_taken,last_watered)
            VALUES (:id,:soil,:temperature,:recording,:watered)""")
        connection.execute(query, {"id": id, "soil": soil, "temperature": temperature, "recording": recording,
                                   "watered": watered})

    connection.execute(sql.text("COMMIT;"))


if __name__ == "__main__":

    load_dotenv()

    plant_dataframe = csv_to_data_frame('./data/cleaned_plant_data.csv')

    connection = create_database_connection(environ)

    insert_into_location_table(connection, plant_dataframe)
    insert_into_botanist_table(connection, plant_dataframe)
    insert_into_plant_table(connection, plant_dataframe)

    insert_into_recordings_table(connection, plant_dataframe)
