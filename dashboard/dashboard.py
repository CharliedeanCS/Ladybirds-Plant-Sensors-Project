"""Script to run the dashboard app, displaying the key plant data for the LNHM botanical wing."""

from os import environ, _Environ

import altair as alt
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Connection, sql
import streamlit as st

COLOUR_LIST = ['#7db16a', '#c6d485', '#618447', '#5e949b', '#415d2e', '#d7f1ec', '#b7c62d', '#0f1511', '#3e6164', '#87c7cd', '#2d4221', '#6a6539' '#2b4242', '#48472f', '#1e2f1d']



def get_db_connection(config: _Environ) -> Connection:
    """Creates a database connection to the SQL Server"""
    engine = create_engine(
        f"mssql+pymssql://{config['DB_USERNAME']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/?charset=utf8")
    conn = engine.connect()
    return conn


def get_data_from_db(conn: Connection) -> pd.DataFrame:
    """Returns a dataframe containing all the food truck data."""
    conn.execute(sql.text("USE plants;"))
    recording_data = conn.execute(sql.text(
        """ SELECT * FROM s_delta.recording 
            LEFT JOIN s_delta.plant 
            ON s_delta.recording.plant_id = s_delta.plant.plant_id
            LEFT JOIN s_delta.botanist
            ON s_delta.plant.botanist_id = s_delta.botanist.botanist_id
            """))

    recordings_df = pd.DataFrame(recording_data.fetchall())
    recordings_df.columns = recording_data.keys()
    recordings_df = recordings_df.loc[:, ~recordings_df.columns.duplicated()].copy()
    print(recordings_df)
    return recordings_df


def get_date_from_data(data: pd.DataFrame) -> pd.DataFrame:
    """Extracts the date from the datetime values for recordings taken."""
    data['date'] = data['recording_taken'].dt.date
    return data


def separate_time_from_datetime(data: pd.DataFrame) -> pd.DataFrame:
    """Extracts the time value from the datetime values for recordings taken. """
    data['time'] = data['recording_taken'].dt.time
    return data


def temp_line_chart(df: pd.DataFrame, selected_plants: list[str]) -> st.altair_chart:
    """Creates a line graph showing temperature of soil throughout the day for plants."""
    df = df[df['name'].isin(selected_plants)].rename(columns={'temperature': 'Soil Temperature', 'time': 'Time'})
    title = alt.TitleParams(
        'Temperature of soil over time', anchor='middle')
    color = alt.Color('name', scale=alt.Scale(range=COLOUR_LIST))
    figure = alt.Chart(df).mark_line().encode(
        x='hoursminutes(Time):T', y='Soil Temperature', color=color).properties(title=title)
    return figure


def moisture_line_chart(df: pd.DataFrame, selected_plants: list[str]) -> st.altair_chart:
    """Creates a line graph showing moisture levels of soil throughout the day for plants."""
    df = df[df['name'].isin(selected_plants)].rename(columns={'soil_moisture': 'Soil Moisture', 'time': 'Time'})
    title = alt.TitleParams(
        'Moisture Level of soil over time', anchor='middle')
    color = alt.Color('name', scale=alt.Scale(range=COLOUR_LIST))
    figure = alt.Chart(df).mark_line().encode(
        x='hoursminutes(Time):T', y='Soil Moisture', color=color).properties(title=title)
    return figure


if __name__ == "__main__":

    # connecting to the database and retrieving the data:
    load_dotenv()
    connection = get_db_connection(environ)
    t_data = get_data_from_db(connection)
    t_data = get_date_from_data(t_data)
    t_data = separate_time_from_datetime(t_data)

    # establishing streamlit dashboard title.
    st.title('LNHM Botanical Plant Sensors')

    # setting up a filter search on the side bar.
    st.sidebar.header('Filter by:')
    chosen_dates = st.sidebar.multiselect("Select Date", t_data['date'].unique(),
                                          default=t_data['date'].unique(), placeholder="Choose an option")
    chosen_plants = st.sidebar.multiselect("Select Plant", t_data['name'].unique(),
                                           default=t_data['name'].unique(), placeholder="Choose an option")

    if chosen_plants and chosen_dates:

        st.subheader('Soil Monitoring', anchor=None, divider='grey')

        st.altair_chart(temp_line_chart
                        (t_data, chosen_plants), theme=None, use_container_width=True)

        st.altair_chart(moisture_line_chart
                        (t_data, chosen_plants), theme=None, use_container_width=True)


