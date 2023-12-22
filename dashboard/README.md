# Dashboard

This folder should contain all code and resources required for dashboard to run.

# Project Description

In order to easily visualise the plant sensor data, a dashboard was created. This allows the botanists to track specific plants and ensure their soil temperature and water levels are normal. As well as track when they were last watered. 

## ![:hammer_and_spanner:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-medium/1f6e0-fe0f@2x.png)Getting Setup

1. Run 'pip install -r requirements.txt'

.env keys used:

- AWS_ACCESS_KEY_ID = xxxxxxxxxx
- AWS_SECRET_ACCESS_KEY = xxxxxxxx
- DB_USERNAME = xxxxxxxx
- DB_PASSWORD = xxxxxxxx
- DB_HOST = xxxxxxxxx
- DB_PORT = xxxxxxxx

## ![🗂](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-medium/1f5c2-fe0f@2x.png) Files Explained

* `dashboard.py`
  * A script to run the dashboard and create all the relevant visualisations using current and archived data.
  * To run locally use the command 'streamlit run dashboard.py'

- `Dockerfile`
  - A script to dockerise the dashboard and enable it to be run as a container either locally or when uploaded to the Elastic Container Repository (ECR) on AWS.
- `.streamlit/config.toml`
  - Details the colour theme for the dashboard when run locally (this is contained in the Dockerfile for image creation, therefore is not a required file when running a container).
