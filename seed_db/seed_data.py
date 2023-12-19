"""Small example of connecting to an MSSQL database."""
import csv
from os import environ

# from dotenv import load_dotenv
# from sqlalchemy import create_engine, sql



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
    """Takes the .csv data and returns the location information for each plant as a list of unique dicts."""
    locations = []
    for plant in csv_data:
        continent = plant['Continent']
        country = plant['Country']
        region = plant['Region']
        locations.append({"region": region, "country": country, "continent": continent})
    
    location_sets = set([tuple(location.items()) for location in locations])
    unique_locations = [dict(i) for i in location_sets]
    return unique_locations

def extract_plant_data(csv_data: list[dict], botanist_data: list[dict], location_data: list[dict]) -> list[dict]:
    """Extracts relevant plant data from .csv and combines with the botanist and location data to give an apporpriate
    list of unique dicts to seed the plant table."""
    plants = []
    for plant in csv_data:
        plant_id = plant['Id']
        name = plant['Name']
        for botanist in botanist_data:
            if plant['Botanist Name'] == botanist['name']:
                botanist_id = botanist_data.index(botanist)+1
        for location in location_data:
            if plant['Region'] == location['region'] and plant['Country'] == location['country']:
                location_id = location_data.index(location)+1
        plants.append({"plant_id": plant_id, "name": name, "botanist_id": botanist_id, "location_id": location_id})
    return plants


if __name__ == "__main__":

    filepath = '../pipeline/cleaned_plant_data.csv'
    data = read_csv(filepath)
    botanists = extract_botanist_data(data)
    locations = extract_location_data(data)
    plants = extract_plant_data(data, botanists, locations)
    print(locations)

    # load_dotenv()

    # engine = create_engine(
    #     f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    # conn = engine.connect()

    # conn.execute(sql.text("USE plants;"))

    # # conn.execute(sql.text("CREATE TABLE general.example (id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY, word TEXT NOT NULL);"))

    # query = sql.text(
    #     "INSERT INTO s_delta.botanist (name, email, telephone_number) VALUES (:msg)")
    # conn.execute(query, {"msg": "Dan"})

    # query = sql.text("SELECT * FROM general.example;")

    # conn.execute(sql.text("COMMIT;"))
    # res = conn.execute(query).fetchall()
    # print(res)
