"""Script to connect to an MSSQL database and insert plant data"""


from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql


def create_database_connection():
    """Creates a database connection to the SQL Server"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    conn = engine.connect()

    return conn


if __name__ == "__main__":

    load_dotenv()

    connection = create_database_connection()

    conn.execute(sql.text("USE plants;"))

    query = sql.text("INSERT INTO general.example (word) VALUES (:msg)")
    conn.execute(query, {"msg": "SQL INJECTION CODE"})

    query = sql.text("SELECT * FROM s_delta.example;")

    conn.execute(sql.text("COMMIT;"))
    res = conn.execute(query).fetchall()
    print(res)
