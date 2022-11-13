from datetime import datetime
from json import load
from os import environ, system
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from app.utils import read_timeseries


def get_api_key():
    """Get BLS API Key"""
    if Path("app/.env").exists():
        load_dotenv()

    key = environ["APIKEY"]

    assert isinstance(key, str)

    return key


def run():
    """
    Run homepage.
    """

    st.title("Labor Indicators")
    
    

    with open("app/BLS_series_mapping.json") as json_file:
        bls_mapping = load(json_file)

    series_choice = st.selectbox("BLS Series ID", tuple(bls_mapping.keys()))
    series_id = bls_mapping[series_choice][0]
    freq_id = bls_mapping[series_choice][1]

    current_year = datetime.now().year

    start_year_options = [str(x) for x in range(1948, int(current_year) + 1)][::-1]
    start_year = st.selectbox("Start Year", start_year_options, index=1)

    end_year_options = [str(x) for x in range(int(start_year), int(current_year) + 1)][
        ::-1
    ]
    
    end_year = st.selectbox("End Year", end_year_options, index=0)

    value_type = ["Level", "Index from Start Year"]
    value_status = st.selectbox("Value Type", value_type, index=0)

    if int(end_year) - int(start_year) > 20:
        raise ValueError("Start and End Years must be a maximum of 20 years apart.")

    system("poetry run streamlit cache clear")

    read_timeseries(
        series_id=series_id,
        series_choice=series_choice,
        value_status=value_status,
        freq=freq_id,
        start_year=start_year,
        end_year=end_year,
        apikey=get_api_key(),
    )
    st.caption("Source: US Dept. of Labor, Bureau of Labor Statistics")
