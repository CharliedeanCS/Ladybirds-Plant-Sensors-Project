"""Basic unit tests for seeding plant, botanist and plant location data into the database."""

from seed_data import extract_botanist_data, extract_location_data, extract_plant_data

TEST_DATA = [{'Botanist Email': 'carl.linnaeus@lnhm.co.uk',
                          'Botanist Name': 'Carl Linnaeus', 'Botanist Phone': '(146)994-1635x35992',
             'last_watered': 'Mon, 18 Dec 2023 14:03:04 GMT', 'Id': 2, 'Name': 'Epipremnum Aureum',
             'Region': 'Resplendor', "Country's Initials": 'BR', 'Continent': 'America'}]
BOTANIST_DATA = [{'name': 'Carl Linnaeus',
                  'telephone_number': '(146)994-1635x35992'}]
LOCATION_DATA = [{'region': 'Resplendor',
                  "country": 'Brazil', 'continent': 'America'}]

def test_extract_botanist_data_works():
    """Testing that the function to extract botanist data returns the correct data."""
    assert extract_botanist_data(TEST_DATA) == [
        {"name": "Carl Linnaeus", "email": "carl.linnaeus@lnhm.co.uk", "telephone_number": "(146)994-1635x35992"}]


def test_extract_unique_botanist_data():
    """Testing that the function only appends unique data to the list."""
    data = [{'Botanist Email': 'carl.linnaeus@lnhm.co.uk',
            'Botanist Name': 'Carl Linnaeus', 'Botanist Phone': '(146)994-1635x35992'}, 
            {'Botanist Email': 'carl.linnaeus@lnhm.co.uk',
            'Botanist Name': 'Carl Linnaeus', 'Botanist Phone': '(146)994-1635x35992'},
            {'Botanist Email': 'random',
            'Botanist Name': 'name', 'Botanist Phone': '1234'}
            ]
    botanist_data = extract_botanist_data(data) 
    assert len(botanist_data) == 2
    assert len(data) == 3
    

def test_extract_location_data_works():
    """Test that the correct information is returned when extracting location data."""
    assert extract_location_data(TEST_DATA) == [{"region": "Resplendor", "country": "Brazil", "continent": "America"}]


def test_extract_plant_data_works():
    """Test that the correct plant information is returned."""
    assert extract_plant_data(TEST_DATA, BOTANIST_DATA, LOCATION_DATA) == [
        {"plant_id": 2, "name": "Epipremnum Aureum", "botanist_num": "(146)994-1635x35992", "location_reg": "Resplendor"}]
