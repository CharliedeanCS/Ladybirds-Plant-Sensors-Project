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

    assert remove_rows_with_null(df, critical_columns).to_dict() == {
        'C': {0: 9, 1: 10, 2: 11, 3: 12}}

# data = {'A': [1, 2, None, 4],
#         'C': [9, 10, 11, 12]}

# df = pd.DataFrame(data)

# df = df.dropna(subset='A')
# print(df)
