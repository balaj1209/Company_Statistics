import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json


st.title("Comapany Stats")

PATH_to_KEY = "Weight.json"
Student_data = "https://docs.google.com/spreadsheets/d/1lyQExfwjbRM24CBJDxEfmEqt2Ah49CYs4_eFsiIX5KE/edit?usp=sharing"
company_data = "https://docs.google.com/spreadsheets/d/14OWSWzvDppYTZR47yydXl5QXQfjMu400HFoOP3I-Imk/edit?usp=sharing"
company_req_data = "https://docs.google.com/spreadsheets/d/1nK-VwPIwqxKBFEb5aFlYCVtVRwmuZfSy9tY4dPs_Cco/edit?usp=sharing"

Data_selector = st.sidebar.selectbox(
    'Select a Data set to be viewed -->',
    ('Student Details', 'Company Details', 'Company Requirements')
)

# Getting the data
@st.cache_data
def connect_to_sheet(url):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(""" {
  "type": "service_account",
  "project_id": "weighty-smoke-436907-p5",
  "private_key_id": "9b7f4737ac796440364d4055ba567246fd9d85f4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDpVh6459tjE31X\nHFjRpeJfnXbmxPY+GjVFhyqonA2YZF9x/SIoIFgUoG1QQQmeDb+aDFEE7P4NaZzR\n9xR38Zoa2J0E9lrHZCsw8rxZoUAkPkV3ihsr3lpT74BcrvzfwSQ5MJ9ljElem+aa\nNI4kio+ZOac7vVlR4v3WjDa3gL4NYxtahdcUhE09wEhtaV5s/7uMP6ZNtv6DAo0Z\nZRFJ9RlmtvMTg7VtYMVa3rsvics23RM0zVLmSpI8eUNbMxrDxIqnW1JDm1LXyW3g\nu31SjZb5QwB9MDgTJbt1h1ZDZxlJTGDAxm8zSW71NV7QuI0I1wrtRdsm5KK8hpOu\n4LmOm6SLAgMBAAECggEATGqW3ymXsMfWOawf7nDsRTIVmZgRqN7+aUnOD7Ajx6+/\njl4/THLjRcYQZsMV+jw4bqPv+LQAs7XN1PmdK3blaDtemRxxOHG2r24ffx8PGY+H\nQpHpOiG05V4/ZJsuV70yNsSUvzYFZUWbbQ8fKhpy0tSNz0PAt8+mIBiFZu1z0H/v\nfxzwREupoybUnt2gL55VpnXdbvEkMIk8Nxh0KXGMIlG4XCiU+/FBZjL5Vu2DHBef\nsqlcmxjeE0VNc7zexcWgWseNb4ITHdWvmNnhRQOwHY830nle0DRDkL4kY58/dnyJ\nZSzMKbBs3C3AwV766BIOI6pXGytXJyN60DyOnu8rwQKBgQD4aN/ASMH8Y7xnzEFJ\nr4XZ3WqBcGIiCCAnET5l/RvCJkRhS536QWeWnplvENCWP20J2opq4JPdmuUO2uxf\nMsiYKfAWcoQUVII5j7yo7CW79Wi7v/uVR0dbpTPZ0YbVnvWrLuu1o579LPb5wWht\nZR/YGl+lzoK/JbkRGMdHcOjxqwKBgQDwd1bHTuoqmjKKYqdMlPCzPVwwPudOOXsV\n4xKITl4D9q17tFlRoYcp2gZ+G/5r+A+hB/8km8q0uZWgtPfZmqQEI0Wcm5PzYe5j\nE+WmN84xI/5F6WH+J3iQWMGikWSQK+tKpKNOPl9zH3A6iWsBP2TTHvF7i2EJz54r\noFQqo/r4oQKBgGWwKMhCAIcdHOcwyhkr7RM+fHb4VnOv99mGSZDeiBp2J8/ccJMd\naxZRXmYE8B5RYIWEHN2biWxSGCp4nAJse4kuwcWuozrfTV/a41QTN282CuWwtYBq\naV+uxQcJqrSQGek1j/APRupFGeUrs1/04ZBJW5Y4b3VoL9Y72nf4VKN5AoGAeGsa\nvtZq94iedKRwqS4Q14GLz/FAPfEVDWHYHwA3nn6CY+dtry5XlILFK5PzNbhUg0yQ\n3ZFS0mv5XTAiygrhxdyv+HwEfCX3jhAhubpKfFtM80+rLe4wNwDrfvCWTohf3NJT\noVQk0m7U8cttFYPchskBHuAuaQ5aY/h3DZ9uh+ECgYEAkSnzZvpkw+QVGcfHce0J\nb75PHgOS/Ym8intnGXRA3RJhuhUV0s+F681CP0kFa6yYbmdSwSVuohLNtPiem4Fo\nLVOtKVbZjpI4uTBZaGrcd89UqWbe70pLGuDq2r2FBpSTq5cWKzO12MYaYSkO8m55\nnpd6rp9F0bwFpM9TwBXdJUY=\n-----END PRIVATE KEY-----\n",
  "client_email": "compan-stats@weighty-smoke-436907-p5.iam.gserviceaccount.com",
  "client_id": "107747295101554922006",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/compan-stats%40weighty-smoke-436907-p5.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}""", scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_url(url).sheet1
        return sheet.get_all_values() #raw data
    
    except Exception as er:
        st.error(f'Error Fetching Data {er}')
        return None

dataset_urls = {
    'Student Details': Student_data,
    'Company Details': company_data,
    'Company Requirements': company_req_data
}

if Data_selector in dataset_urls:
    raw_data = connect_to_sheet(dataset_urls[Data_selector])
else:
    st.write('Please select a valid dataset.')

# Loading the data
@st.cache_data
def process_data(data):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

st.subheader(f"{Data_selector} Viewer")

if raw_data:
    df = process_data(raw_data)
    st.dataframe(df)
    st.write(f'Number of Rows: {df.shape[0]}')
    st.write(f'Number of Columns {df.shape[1]}')

    with st.expander('Data Summary', expanded=False):
        st.subheader('Data Summary')
        st.dataframe(df.describe().T)

    with st.expander('Filter Data', expanded=False):
        st.subheader("Filter Data")
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter by", columns)
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox("Select value", unique_values)      

        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)
        st.write(f' Number Of ROWS {filtered_df.shape[0]}')    

    if Data_selector == 'Student Details':
        st.subheader('Data Visulization')

        with st.expander('Gender Distribution ', expanded=False):
            #st.write('Gender Distribution')
            fig, ax = plt.subplots()
            sns.countplot(x = 'Gender', data=df)
            ax.set_xlabel('Gender')
            ax.set_ylabel('Count of Gender')
            plt.xticks(rotation = 90)
            st.pyplot(fig)

        with st.expander('Course Selection', expanded=False):
            #st.write('Gender Distribution')
            fig, ax = plt.subplots()
            sns.countplot(x = 'Course_enrolled', data=df)
            ax.set_xlabel('Course enrolled by students')
            ax.set_ylabel('Count of Students')
            plt.xticks(rotation = 90)
            st.pyplot(fig)







#if st.button("Generate Plot"):
# st.line_chart(df.set_index(x_column)[y_column])
# st.bar_chart(df.set_index(x_column)[y_column])
# st.area_chart(df.set_index(x_column)[y_column])
# st.(df.set_index(x_column)[y_column])

# if st.button("Generate Plot"):
#     fig, ax = plt.subplots()
#     ax.plot(df.set_index(x_column)[y_column])
#     st.pyplot(fig)

