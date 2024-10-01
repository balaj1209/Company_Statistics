

st.title("Comapany Stats")


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

crediential = service_account.Credentials.from_service_account_info(st.secrets['gcp_service_account'],scopes = scope)

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
        #creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_to_KEY, scope)
        client = gspread.authorize(crediential)

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

