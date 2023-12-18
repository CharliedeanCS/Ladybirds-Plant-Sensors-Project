import pandas as pd
from datetime import datetime

from transform import standardize_country_name, remove_rows_with_null, check_soil_temp_valid, check_soil_moisture_valid, normalize_datetimes


def test_standardize_country_name():
    assert standardize_country_name('UK') == 'United Kingdom'


def test_standardize_country_name_2():
    assert standardize_country_name('US') == 'United States'


def test_standardize_country_name_3():
    assert standardize_country_name('FR') == 'France'


def test_standardize_country_name_4():
    assert standardize_country_name('CL') == 'Chile'


def test_remove_rows_with_null():
    data = {'A': [None, 2, 1, 4],
            'B': [5, None, 7, 8],
            'C': [9, 10, 11, 12]}

    df = pd.DataFrame(data)
    critical_columns = ['A', 'B']

    df = remove_rows_with_null(df, critical_columns)
    assert df.to_dict() == {'A': {2: 1.0, 3: 4.0},
                            'B': {2: 7.0, 3: 8.0},
                            'C': {2: 11.0, 3: 12.0}}


def test_check_soil_temp_valid():
    data = {'Plant Name': ['PlantA', 'PlantB', 'PlantC', 'PlantD'],
            'Temperature': [-4, 101, 15, 31]}

    df = pd.DataFrame(data)

    df = check_soil_temp_valid(df)

    assert df.to_dict() == {'Plant Name': {2: 'PlantC'},
                            'Temperature': {2: 15.0}}


def test_check_soil_moisture_valid():
    data = {'Plant Name': ['PlantA', 'PlantB', 'PlantC'],
            'Soil Moisture': [-4, 101, 15]}

    df = pd.DataFrame(data)

    df = check_soil_moisture_valid(df)

    assert df.to_dict() == {'Plant Name': {2: 'PlantC'},
                            'Soil Moisture': {2: 15.0}}
