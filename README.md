# Ladybirds-Plant-Sensors-Project

## Project Description
The Liverpool Natural History Museum (LNHM) has opened a new botanical wing. This will feature exhibits that showcase a diversity of plants across different regions of the world. This is naturally difficult to maintain, so the museum has set up plant sensors which monitor the health of each plant. However, this is only configured with a single API endpoint, so the aim of the proejct is to help monitor a plants health overtime, store the historical data and create visualisations of the plants health for the gardeners. 

To do this, the team will:
- Create an ETL Pipeline for the plants sensors data.
- Create long term and short term storage solutions for data.
- Visualise data in real time and view data in long term storage.

Terraform:
This project contains a terraform folder that has the capability to to provision the infrastructure of the pipeline.

## Repository Contents
- pipeline
  - database
    - schema.sql
    - db_connect.sh
    - reset_db.sh
  - extract.py
  - test_extract.py
  - transform.py
  - test_transform.py
  - load.py
  - test_load.py
  - pipeline.py
 - terraform
  - main.tf
  - variables.tf


## Setup

1. Navigate to the `pipeline` folder
2. Create and activate a new virtual environment
3. Run `pip3 install -r requirements.txt` to install the required libraries

In the `pipeline` folder and `database` folder a .env file must be made.
This file should contain the keys:
`DB_HOST`
`DB_PORT`
`DB_USERNAME`
`DB_PASSWORD`
`DB_NAME`

In the `terraform` folder a .tfvars file must be made.
This file should contain the variables:
`database_ip`
`database_port`
`database_username`
`database_password`
`database_name`

## Running the script

Run the pipelne with `python3 pipeline.py`; you must be in the `pipeline` folder

## Credits
- Charlie Dean
- Harvind Grewal
- Zander Snow
- Shivani Patel
