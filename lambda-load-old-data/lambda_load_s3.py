"""Script that selects data from previous day in RDS database and inserts it into lnhm_archive.csv file in S3 bucket"""

import csv
from os import environ, path

from boto3 import client
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, engine


def get_database_connection() -> engine.base.Connection:
    """Get a connection to the short term database"""
    sql_engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    connection = sql_engine.connect()

    return connection


def get_s3_client() -> client:
    """Get a connection to the relevant S3 bucket"""
    s3_client = client("s3",
                       aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])
    return s3_client


def extract_old_data_from_database(connection: engine.base.Connection) -> list[tuple]:
    """Extract data older than a day from short-term-memory as a list"""

    connection.execute(sql.text("USE plants;"))

    # Assuming 's_delta' is the schema and 'recording' is the table
    query = sql.text("""
                     SELECT * FROM s_delta.recording
                     WHERE recording_taken < GETDATE();
                     """)

    result = connection.execute(query).fetchall()

    return result


def write_list_of_tuples_to_csv(data: list[tuple], csv_filename: str = 'data/latest_data.csv') -> bool:
    """Write a list of tuples to a CSV file"""

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Assuming the first tuple in the list contains column headers
        if data:
            csv_writer.writerows(data)


def get_master_archive_csv(s3_client: client, bucket: str, folder_name: str):
    """Load archive csv file"""

    contents = s3_client.list_objects(Bucket=bucket)["Contents"]
    all_keys = [o["Key"] for o in contents]

    for k in all_keys:
        if k.endswith('.csv'):
            s3_client.download_file(bucket, k, f"{folder_name}/{k}")


def combine_csv_files(source_csv: str, target_csv: str):
    """Insert previous days data into archive csv"""
    # Read data from the source CSV file
    with open(source_csv, 'r', newline='', encoding='utf-8') as source_file:
        source_reader = csv.reader(source_file)
        source_data = list(source_reader)

    # Append data to the target CSV file
    with open(target_csv, 'a', newline='', encoding='utf-8') as target_file:
        target_writer = csv.writer(target_file)
        target_writer.writerows(source_data)


def load_combined_archive_data_to_s3(s3_client, file_name, bucket, object_name=None):
    """Load old data as csv from short-term-memory into S3 then delete csv file"""

    if object_name is None:
        object_name = path.basename(file_name)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError:
        return False
    return True


def handler(event=None, context=None):
    """Lambda handler function"""
    load_dotenv()

    conn = get_database_connection()
    s3_client = get_s3_client()

    # Retrieve yesterdays data from short-term database
    latest_recording_data = extract_old_data_from_database(conn)

    # Write yesterdays daa to csv into LOCAL_OUTPUT_DIR
    write_list_of_tuples_to_csv(latest_recording_data, 'data/latest_data.csv')

    # Retrieve master archive csv
    get_master_archive_csv(
        s3_client, environ['ARCHIVE_BUCKET'], "./data/")

    # Append latest data csv to archive csv
    combine_csv_files('data/latest_data.csv', 'data/lnhm_archive.csv')

    # Upload new archive file
    load_combined_archive_data_to_s3(s3_client, 'data/lnhm_archive.csv',
                                     environ['ARCHIVE_BUCKET'])


if __name__ == "__main__":

    handler()
