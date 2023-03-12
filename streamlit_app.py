import streamlit as st
import psycopg2
import pandas as pd

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)

# Function to fetch data from database
def fetchData(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        return rows

# Build Streamlit dataframe
def buildTable(data):
    headers = [x[0] for x in data.description]
    rows = [list(row) for row in data]
    return pd.DataFrame(rows, columns=headers)

# Query data from database
query = "SELECT * FROM mytable"
data = fetchData(query)

# Build Streamlit dataframe and display
df = buildTable(data)
st.dataframe(df)
