"""Script that selects data from previous day in RDS database and inserts it into lnhm_archive.csv file in S3 bucket."""

import csv
from io import StringIO
from os import environ, path, _Environ

import pandas as pd
from boto3 import client
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Connection

ARCHIVE_BUCKET = "c9-ladybird-lnhm-data-bucket"
ARCHIVE_KEY = 'lmnh_plant_data_archive.csv'


def get_database_connection(config: _Environ) -> Connection:
    """Get a connection to the short term database."""
    sql_engine = create_engine(
        f"mssql+pymssql://{config['DB_USERNAME']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/?charset=utf8")

    connection = sql_engine.connect()

    return connection


def get_s3_client(config: _Environ) -> S3Client:
    """Get a connection to the relevant S3 bucket."""
    s3_client = client("s3",
                       aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"])
    return s3_client


def extract_old_data_from_database(connection: Connection) -> pd.DataFrame:
    """Extract data older than a day from short-term-memory as a list."""

    connection.execute(sql.text("USE plants;"))

    # Assuming 's_delta' is the schema and 'recording' is the table
    query = sql.text("""
                     SELECT rec.recording_id, rec.soil_moisture, rec.temperature, rec.recording_taken, rec.last_watered,
                        plant.name AS plant_name, bot.name, bot.email, bot.telephone_number, loc.region, loc.country, loc.continent
                        FROM s_delta.recording AS rec
                        JOIN s_delta.plant AS plant ON rec.plant_id = plant.plant_id
                        JOIN s_delta.botanist AS bot ON plant.botanist_id = bot.botanist_id
                        JOIN s_delta.location AS loc ON plant.location_id = loc.location_id
                        WHERE rec.recording_taken < GETDATE();
                     """)

    result = connection.execute(query).fetchall()

    return pd.DataFrame(result).rename(columns={"recording_id": "Recording ID", "soil_moisture": "Soil Moisture", "temperature": "Temperature", "recording_taken": "Recording Taken", "last_watered": "Last Watered",
                                                "plant_name": "Plant Name", "name": "Botanist Name", "email": "Botanist Email", "telephone_number": "Botanist Phone Number", "region": "Region", "country": "Country", "continent": "Continent"})


def refactor_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Changes the column names in the dataframe."""

    return dataframe.rename(columns={"recording_id": "Recording ID", "soil_moisture": "Soil Moisture", "temperature": "Temperature", "recording_taken": "Recording Taken", "last_watered": "Last Watered",
                                     "plant_name": "Plant Name", "name": "Botanist Name", "email": "Botanist Email", "telephone_number": "Botanist Phone Number", "region": "Region", "country": "Country", "continent": "Continent"})


# def write_list_of_tuples_to_csv(data: list[tuple], csv_filename: str = 'data/latest_data.csv') -> bool:
#     """Write a list of tuples to a CSV file"""

#     with open(csv_filename, 'w', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)

#         # Assuming the first tuple in the list contains column headers
#         if data:
#             csv_writer.writerows(data)


# def get_master_archive_csv(s3_client: client, bucket: str, folder_name: str):
#     """Load archive csv file"""

#     contents = s3_client.list_objects(Bucket=bucket)["Contents"]
#     all_keys = [o["Key"] for o in contents]

#     for k in all_keys:
#         if k.endswith('.csv'):
#             s3_client.download_file(bucket, k, f"{folder_name}/{k}")


# def combine_csv_files(source_csv: str, target_csv: str):
#     """Insert previous days data into archive csv"""
#     # Read data from the source CSV file
#     with open(source_csv, 'r', newline='', encoding='utf-8') as source_file:
#         source_reader = csv.reader(source_file)
#         source_data = list(source_reader)

#     # Append data to the target CSV file
#     with open(target_csv, 'a', newline='', encoding='utf-8') as target_file:
#         target_writer = csv.writer(target_file)
#         target_writer.writerows(source_data)


# def load_combined_archive_data_to_s3(s3_client, file_name, bucket, object_name=None):
#     """Load old data as csv from short-term-memory into S3 then delete csv file"""

#     if object_name is None:
#         object_name = path.basename(file_name)

#     try:
#         s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError:
#         return False
#     return True


def get_archive_data_csv(s3_client: S3Client, bucket: str, key: str) -> pd.DataFrame:
    """Retrieves the archived data from an S3 bucket."""

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    csv_str = obj["Body"].read().decode()
    return pd.read_csv(StringIO(csv_str))


def update_archive_data(arch_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """Updates the archived dataframe with new data."""

    return pd.concat([arch_df, new_df], ignore_index=True, sort=False)


def delete_data_from_db(conn: Connection) -> None:
    """Deletes all data from the database."""

    conn.execute()


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection(environ)
    s3_client = get_s3_client(environ)

    arch_data = get_archive_data_csv(s3_client, ARCHIVE_BUCKET, ARCHIVE_KEY)

    new_plant_data = extract_old_data_from_database(conn)

    combined_data = update_archive_data(arch_data, new_plant_data)

    combined_data.to_csv('combined.csv', index=False)

    # combined_data.to_csv(
    #     f"s3://{ARCHIVE_BUCKET}/test.csv", index=False
    # )


# def handler(event=None, context=None):
#     """Lambda handler function"""

#     load_dotenv()

#     conn = get_database_connection(environ)
#     s3_client = get_s3_client(environ)

#     arch_data = get_archive_data_csv(s3_client, ARCHIVE_BUCKET, ARCHIVE_KEY)

#     # Retrieve yesterdays data from short-term database
#     latest_recording_data = extract_old_data_from_database(conn)

#     latest_recording_data = refactor_df(latest_recording_data)

#     combined_data = update_archive_data(arch_data, latest_recording_data)

#     combined_data.to_csv(
#         f"s3://{ARCHIVE_BUCKET}/{ARCHIVE_KEY}", index=False
#     )

#     combined_data.to_csv('combined.csv', index=False)

#     # Write yesterdays daa to csv into LOCAL_OUTPUT_DIR
#     # write_list_of_tuples_to_csv(latest_recording_data, 'data/latest_data.csv')
#     # Retrieve master archive csv
#     # get_master_archive_csv(
#     #     s3_client, environ['ARCHIVE_BUCKET'], "./data/")
#     # Append latest data csv to archive csv
#     # combine_csv_files('data/latest_data.csv', 'data/lnhm_archive.csv')
#     # Upload new archive file
#     # load_combined_archive_data_to_s3(s3_client, 'data/lnhm_archive.csv',
#     #                                  environ['ARCHIVE_BUCKET'])
# if __name__ == "__main__":

#     handler()
