import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import oracledb

def load_data(query):
    user = 'system'
    password = 'arich'
    host = 'localhost'
    port = 1521
    sid = 'xe'

    dsn = oracledb.makedsn(host, port, sid)
    conn_str = f'oracle+oracledb://{user}:{password}@{dsn}'

    engine = create_engine(conn_str)

    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        engine.dispose()  # Ensure the connection is properly closed

# Streamlit app layout
st.title("🎈 My New App")
st.write("Loading data from the database...")

# Load data from the Oracle database
data = load_data('SELECT * FROM cat')

# Display the DataFrame using Streamlit
if not data.empty:
    st.write(data)
else:
    st.write("No data available or there was an error loading the data.")
