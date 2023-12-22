# Pipeline

This folder should contain all code and resources required for the pipeline.

# Project Description

- This folder contains all the information needed to transfer all data from an RDS to a CSV file in an S3 bucket.

## 🛠️ Getting Setup
- Install requirements using `pip3 install -r requirements.txt`
- Install boto3 type hints by running `python -m pip install 'boto3-stubs[essential]'`
- Create a `.env` file with the following information:
    - AWS_ACCESS_KEY_ID = xxxxxxxxxx
    - AWS_SECRET_ACCESS_KEY = xxxxxxxx
    - DB_USERNAME = xxxxxxxx
    - DB_PASSWORD = xxxxxxxx
    - DB_HOST = xxxxxxxxx
    - DB_PORT = xxxxxxxx

## 🗂️ Files Explained
- `transfer_old_data.py`
    - A script to extract all data from an RDS and load it onto a CSV file contained within an S3 bucket. After this, the script removes all the data from the RDS.
- `test_transfer_old_data.py`
    - A script containing unit tests for the `transfer_old_data.py` script
- `Dockerfile`
    - 
