"""Small example of connecting to an MSSQL database."""
import csv
from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Connection

from transform import standardize_country_name


def get_connection()-> Connection:
    """Returns a connection to the database."""
    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USERNAME']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")
    connection = engine.connect()
    return connection

def read_csv(file_path: str) -> list[dict]:
    """Extracts the relevant information about botanists from the plant data,
    Appends to a list to seed the 'botanist' table."""
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def extract_botanist_data(csv_data: list[dict]) -> list[dict]:
    """Takes the .csv data and returns relevant botanist information as a list of unique dicts."""
    botanists = []
    for plant in csv_data:
        name = plant['Botanist Name']
        email = plant['Botanist Email']
        telephone_number = plant['Botanist Phone']
        botanists.append({"name": name, "email": email, "telephone_number": telephone_number})

    botanist_sets = set([tuple(botanist.items()) for botanist in botanists])
    unique_botanists = [dict(i) for i in botanist_sets]
    return unique_botanists


def extract_location_data(csv_data: list[dict]) -> list[dict]:
    """Takes the cleaned .csv data, returns the location 
    information for each plant as a list of unique dicts."""
    locations = []
    for plant in csv_data:
        continent = plant['Continent']
        country = standardize_country_name(plant["Country's Initials"])
        region = plant['Region']
        locations.append({"region": region, "country": country, "continent": continent})

    location_sets = set([tuple(location.items()) for location in locations])
    unique_locations = [dict(i) for i in location_sets]
    return unique_locations


def extract_plant_data(csv_data: list[dict], botanist_data: list[dict], location_data: list[dict]) -> list[dict]:
    """Extracts relevant plant data from the cleaned .csv file, combines with the 
    botanist and location data, returns a list of unique dicts to seed the plant table."""
    plants = []
    for plant in csv_data:
        plant_id = plant["Id"]
        name = plant['Name']
        for botanist in botanist_data:
            if plant['Botanist Name']== botanist['name']:
                botanist_num = botanist['telephone_number']
        for location in location_data:
            if plant['Region'] == location['region']:
                location_reg = location['region']

        plants.append({"plant_id": plant_id, "name": name, "botanist_num": botanist_num, "location_reg": location_reg})
    return plants


def seed_botanist_table(conn: Connection, botanist_data: list[dict]) -> None:
    """Seed the botanist table with the botanist data list."""
    for botanist in botanist_data:
        query = sql.text("INSERT INTO s_delta.botanist (name, email, telephone_number) VALUES (:n, :e, :t)")
        args = ({"n":botanist["name"], "e":botanist["email"], "t":botanist["telephone_number"]})
        conn.execute(query,args)



def seed_location_table(conn: Connection, location_data: list[dict]) -> None:
    """Seed the location table with the location data list."""
    for location in location_data:
        query = sql.text(
            "INSERT INTO s_delta.location (region, country, continent) VALUES (:reg, :cou, :con)")
        args = ({"reg": location["region"], "cou": location["country"],
                "con": location["continent"]})
        conn.execute(query, args)



def seed_plant_table(conn: Connection, plant_data: list[dict]) -> None:
    """Seed the plant table with the plant data list and relevant botanist and location ids."""
    for plant in plant_data:
        query = sql.text("SELECT botanist_id FROM s_delta.botanist WHERE telephone_number = (:num)")
        args = ({"num": plant["botanist_num"]})
        botanist_id = conn.execute(query,args).fetchone()[0]

        query = sql.text(
            "SELECT location_id FROM s_delta.location WHERE region = (:reg)")
        args = ({"reg": plant["location_reg"]})
        location_id = conn.execute(query, args).fetchone()[0]

        query = sql.text(
            "INSERT INTO s_delta.plant (plant_id, name, botanist_id, location_id) VALUES (:id, :n, :b_id, :l_id)")
        args = ({"id": plant["plant_id"],"n": plant["name"], "b_id": botanist_id,
                "l_id": location_id})
        conn.execute(query, args)

    conn.execute(sql.text("COMMIT;"))


if __name__ == "__main__":
    load_dotenv()

    #extracting data from .csv file
    filepath = 'data/plant_data.csv'
    data = read_csv(filepath)
    botanists = extract_botanist_data(data)
    locations = extract_location_data(data)
    plants = extract_plant_data(data, botanists, locations)

    #connecting to database
    db_conn = get_connection()
    db_conn.execute(sql.text("USE plants;"))

    #seeding each table with relevant data
    seed_botanist_table(db_conn, botanists)
    seed_location_table(db_conn,locations)
    seed_plant_table(db_conn, plants)

    db_conn.close()
