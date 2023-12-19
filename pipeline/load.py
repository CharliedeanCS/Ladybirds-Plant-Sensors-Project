"""Script to connect to an MSSQL database and insert plant data"""


from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Connection
import pandas as pd

from transform import csv_to_data_frame


def create_database_connection() -> Connection:
    """Creates a database connection to the SQL Server"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    conn = engine.connect()

    return conn


def insert_into_recordings_table(connection: Connection, plant_data: pd.DataFrame) -> None:
    """Inserts data from a pandas data frame into a SQL Server"""

    plant_list = plant_data.values.tolist()

    for plant in plant_list:

        id = plant[0]
        soil = plant[4]
        temperature = plant[5]
        recording = plant[3]
        watered = plant[2]

        print(id)

        connection.execute(sql.text("USE plants;"))

        query = sql.text(
            """INSERT INTO s_delta.recording (plant_id,soil_moisture,temperature,recording_taken,last_watered)
            VALUES (:id,:soil,:temperature,:recording,:watered)""")
        connection.execute(query, {"id": id, "soil": soil, "temperature": temperature, "recording": recording,
                                   "watered": watered})
        break
    connection.execute(sql.text("COMMIT;"))


if __name__ == "__main__":

    load_dotenv()

    plant_dataframe = csv_to_data_frame('./data/cleaned_plant_data.csv')

    connection = create_database_connection()

    insert_into_recordings_table(connection, plant_dataframe)
