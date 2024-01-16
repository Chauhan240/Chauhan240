import streamlit as st
import pandas as pd
import json

# Load data
json_file_path = r"hyperlinks_data.json"
file_path = r"Consulting Latest Jobs-Deloitte.xlsx"

# Load Excel file
xl = pd.ExcelFile(file_path)

# Read JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extract sheet names
sheet_names = xl.sheet_names

# Clean up function for keys in JSON
def clean_up_key(key):
    return key.encode('utf-8').decode('unicode_escape')

# Dropdown for selecting sheet
selected_sheet = st.sidebar.selectbox("Select Department", sheet_names)

# Display data for selected sheet
st.header(f"Selected Department: {selected_sheet}")

# Read data from Excel
df = xl.parse(selected_sheet)

# Check if 'External - Job Portal Link' column exists
if 'External - Job Portal Link' in df.columns:
    # Create a new column 'Clickable Link' with HTML-formatted hyperlinks
    df['External - Job Portal Link'] = df['External - Job Portal Link'].apply(lambda x: f'<a href="{data[selected_sheet].get(clean_up_key(x), "#")}">{x}</a>')

    # Display 'External - Job Portal Link' and 'Keywords' columns with clickable links
    st.write(df[['External - Job Portal Link', 'Keywords']].to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write("Column 'External - Job Portal Link' not found in the sheet.")
