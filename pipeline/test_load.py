"""Unit tests created to ensure the functionality of the load script."""
from unittest.mock import MagicMock, patch

from load import insert_into_location_table
from transform import csv_to_data_frame


# def test_insert_into_location_table():
#     """Tests that the insert into location table works correctly."""

#     mock_connection = MagicMock()
#     mock_execute = mock_connection.execute().fetchone()

#     plant_dataframe = csv_to_data_frame('./data/cleaned_plant_data.csv')

#     print(plant_dataframe)

#     assert 1 == 0
