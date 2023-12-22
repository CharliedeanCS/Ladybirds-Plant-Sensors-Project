# Dashboard

This folder should contain all code and resources required for dashboard to run.

# Project Description

In order to easily visualise the plant sensor data, a dashboard was created. This allows the botanists to track specific plants and ensure their soil temperature and water levels are normal. As well as track when they were last watered. 

## ![:hammer_and_spanner:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-medium/1f6e0-fe0f@2x.png)Getting Setup

'pip install -r requirements.txt'

.env keys used:
AWS_ACCESS_KEY_ID = xxxxxxxxxx
AWS_SECRET_ACCESS_KEY = xxxxxxxx
DB_USERNAME = xxxxxxxx
DB_PASSWORD = xxxxxxxx
DB_HOST = xxxxxxxxx
DB_PORT = xxxxxxxx

## ![🗂](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-medium/1f5c2-fe0f@2x.png) Files Explained

- `extract.py`
    - A script to extract data from the truck s3 bucket located on AWS

- `transform.py`
  - A script to merge and clean all the data found in a csv file to ensure its the correct format and contains the correct information.
- `load.py`
  - A script to load the cleaned csv output into a redshift cluster.
- `pipeline.py`
  - A script to load a CSV output into a Redshift Cluster.
  - Cleans the data (Making sure its in the correct format)
  - Uploads the data to a Redshift Cluster.
  - Arguments:
    - --rows : Enter the amount of rows you would like to upload to the database
