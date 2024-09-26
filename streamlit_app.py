import streamlit as st

import pandas as pd


from sqlalchemy import create_engine
import oracledb

def load_data(querry):
    user = 'system'
    password = 'arich'
    host = 'localhost'
    sid = 'xe'

    dsn = oracledb.makedsn(host=host, port=1521, sid=sid)
    conn_str = f'oracle+oracledb://{user}:{password}@{dsn}'
    engine = create_engine(conn_str)

    try:
        df = pd.read_sql(querry, engine)
        return df

    except  Exception as e:
        st.error(f'Error loading data {e}')

    finally:
        engine.dispose()
        print('connected')

    
    


st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

data = load_data('select * from cat')
st.write(data)