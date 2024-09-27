import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import oracledb


import json
import airbyte as ab
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from itertools import islice
from plotly.subplots import make_subplots


# Streamlit app layout
st.title("🎈 My New App")
st.write("Loading data from the database...")

# Load data from the Oracle database

