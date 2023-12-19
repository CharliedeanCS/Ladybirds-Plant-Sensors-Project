"""Script to connect to an MSSQL database and insert plant data"""


from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Connection
import pandas as pd


def create_database_connection() -> Connection:
    """Creates a database connection to the SQL Server"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    conn = engine.connect()

    return conn


def insert_into_recordings_table(connection: Connection, plant_data: pd.DataFrame) -> None:
    """Inserts data from a pandas data frame into a SQL Server"""

    connection.execute(sql.text("USE plants;"))

    query = sql.text("INSERT INTO s_delta.recording (word) VALUES (:msg)")
    connection.execute(query, {"msg": "SQL INJECTION CODE"})
    connection.execute(sql.text("COMMIT;"))


if __name__ == "__main__":

    load_dotenv()

    plant_dataframe = pd.read_csv("plant_data.csv")

    connection = create_database_connection()
