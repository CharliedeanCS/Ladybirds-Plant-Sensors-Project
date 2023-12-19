import csv

from boto3 import client
from botocore.exceptions import ClientError
from os import environ, listdir
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, engine
from datetime import datetime, timedelta

LOCAL_OUTPUT_DIR = "./data/"
S3_OUTPUT_DIR = "c9-harvind-output/"


def get_database_connection() -> engine.base.Connection:
    """Get a connection to the short term database"""
    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    connection = engine.connect()

    return connection


def get_s3_client() -> client:
    """Get a connection to the relevant S3 bucket"""
    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])
    return s3


def extract_old_data_from_database(connection: engine.base.Connection):
    """Extract data older than a day from short-term-memory as csv file"""

    connection.execute(sql.text("USE plants;"))

    current_date = datetime.now().date()

    # Assuming 's_delta' is the schema and 'recording' is the table
    query = sql.text("""
                     SELECT * FROM s_delta.recording
                     WHERE CONVERT(DATE, recording.recording_taken) < :today;
                     """)

    result = connection.execute(
        query, {'today': current_date}).fetchall()

    return result


def write_list_of_tuples_to_csv(data: list[tuple], csv_filename: str = 'latest_data.csv') -> bool:
    """Write a list of tuples to a CSV file"""

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Assuming the first tuple in the list contains column headers
        if data:
            csv_writer.writerows(data)



def get_master_archive_csv(s3_client:client, bucket:str, folder_name:str):
    """Load archive csv file""" 
    
    contents = s3_client.list_objects(Bucket=bucket)["Contents"]
    all_keys = [o["Key"] for o in contents]
    
    # new_k = k[17:]

    for k in all_keys:
        if k.endswith('.csv'):
            s3_client.download_file(bucket, k, f"{folder_name}/{k}")

def load_combined_archive_data_to_s3(s3_client, file_name, bucket, object_name=None):
    """Load old data as csv from short-term-memory into S3 then delete csv file"""
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def handler(event=None, context=None):
    """Lambda handler function"""
    load_dotenv()
    pass


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()
    s3_client = get_s3_client()
    
    # Retrieve yesterdays data from short-term database
    list_of_recording_data = extract_old_data_from_database(conn)

    # Write yesterdays daa to csv into LOCAL_OUTPUT_DIR
    write_list_of_tuples_to_csv(list_of_recording_data, 'latest_data.csv')

    # Retrieve master archive csv
    get_master_archive_csv(s3_client, environ['ARCHIVE_BUCKET'], LOCAL_OUTPUT_DIR)

    # Append latest data csv to archive csv



    file_name = LOCAL_OUTPUT_DIR + ''.join([x for x in listdir(LOCAL_OUTPUT_DIR) if x.endswith('.csv')])
    object_name = 

    load_old_data_to_s3(s3_client, file_name,
                        environ['ARCHIVE_BUCKET'], object_name)
