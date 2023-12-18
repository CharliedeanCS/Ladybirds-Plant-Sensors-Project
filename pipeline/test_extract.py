"""Basic unit tests for the extracting from API functions"""

import pytest
from unittest.mock import patch
import requests.exceptions

import pandas as pd

from extract import flatten_and_organize_data, convert_plant_data_to_csv, fetch_plant_data


TEST_DATA = {'botanist': {'email': 'carl.linnaeus@lnhm.co.uk',
                          'name': 'Carl Linnaeus', 'phone': '(146)994-1635x35992'},
             'last_watered': 'Mon, 18 Dec 2023 14:03:04 GMT', 'name': 'Epipremnum Aureum',
             'origin_location': ['-19.32556', '-41.25528', 'Resplendor', 'BR', 'America/Sao_Paulo'],
             'plant_id': 50, 'recording_taken': '2023-12-18 14:50:56', 'scientific_name':
             ['Epipremnum aureum'], 'soil_moisture': 97.21896240755082,
             'temperature': 13.231052699244547}


def test_flatten_and_organize_data():
    """
    Tests that the flatten and organize dataset functions works as
    intended and returns a new dict.
    """

    output_dict = flatten_and_organize_data(TEST_DATA)

    assert isinstance(output_dict, dict)

    assert output_dict["Botanist Email"] == "carl.linnaeus@lnhm.co.uk"


def test_flatten_and_organize_data_empty():
    """Tests that an error raises if the data is empty."""

    with pytest.raises(ValueError):
        flatten_and_organize_data({})


def test_convert_plant_data_returns_correct_format():
    """Tests the convert plant data file returns a pandas data frame"""

    df = convert_plant_data_to_csv([TEST_DATA])

    assert isinstance(df, pd.DataFrame)


def test_fetch_plant_data_fails_at_51(mock_get):
    mock_get.return_value = {}

    response = fetch_plant_data(1)

    print(response)

    assert 1 == 0
