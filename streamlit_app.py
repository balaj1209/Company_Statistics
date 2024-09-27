import streamlit as st
import pandas as pd
import json
import airbyte as ab
import pandas as pd

import streamlit as st
from datetime import datetime
from itertools import islice



# Streamlit app layout
st.title("🎈 My New App")
st.write("Loading data from the database...")

PATH_to_KEY = r"E:\Mishal\Ds_project\Case_study\New folder\Analysis\weighty-smoke-436907-p5-9b7f4737ac79.json"
URL_to_SPREADSHEET = "https://docs.google.com/spreadsheets/d/1lyQExfwjbRM24CBJDxEfmEqt2Ah49CYs4_eFsiIX5KE/edit?usp=sharing"

@st.cache_data
def _read_service_account_secret():
    with open(PATH_to_KEY) as f:
        return json.load(f)
    

@st.cache_resource
def connect_to_gsheets():
    s_acc = _read_service_account_secret()
    gsheets_connection = ab.get_source(
        "source-google-sheets",
        config={
            "spreadsheet_id": URL_to_SPREADSHEET,
            "credentials": {
                "auth_type": "Service",
                "service_account_info": json.dumps(s_acc),
            },
        },
    )
    # gsheets_connection.check()  # can use to check network

    gsheets_connection.select_all_streams()
    # gsheets_connection.select_streams("ticker")  # select stream to sync
    
    return gsheets_connection

@st.cache_data
def download_data(_gsheets_connection):
    airbyte_streams = _gsheets_connection.read()

    ticker_df = airbyte_streams["ticker"].to_pandas()

    history_dfs = {}
    for ticker in list(ticker_df["ticker"]):
        d = airbyte_streams[ticker].to_pandas()
        history_dfs[ticker] = d

    return ticker_df, history_dfs
