from boto3 import client
from botocore.exceptions import ClientError
from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, engine


def get_database_connection() -> engine.base.Connection:
    """Get a connection to the short term database"""
    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    connection = engine.connect()

    return connection


def get_s3_connection():
    """Get a connection to the relevant S3 bucket"""
    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])
    return s3


def extract_old_data_from_database(connection):
    """Extract data older than a day from short-term-memory as csv file"""
    pass


def load_old_data_to_s3():
    """Load old data as csv from short-term-memory into S3 then delete csv file"""
    pass


def handler(event=None, context=None):
    """Lambda handler function"""
    load_dotenv()
    pass


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    conn.execute(sql.text("USE plants;"))

    query = sql.text("SELECT * FROM s_delta.botanist;")
    conn.execute(sql.text("COMMIT;"))

    res = conn.execute(query).fetchall()
    print(res)
