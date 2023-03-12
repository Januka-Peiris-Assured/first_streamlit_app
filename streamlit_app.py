import snowflake.connector
import streamlit as st

# Snowflake login credentials
account = st.secrets["account"]
username = st.secrets["username"]
password = st.secrets["password"]

# Create a connection object
conn = snowflake.connector.connect(
    account=account,
    user=username,
    password=password,
)

# Get a cursor object
cur = conn.cursor()

# Get virtual warehouses
cur.execute("SHOW WAREHOUSES")
warehouse_names = [row[1] for row in cur.fetchall()]

# Get databases
cur.execute("SHOW DATABASES")
database_names = [row[1] for row in cur.fetchall()]

# Get schemas
cur.execute("SHOW SCHEMAS")
schema_names = [row[2] for row in cur.fetchall()]

# Get tables
cur.execute("SHOW TABLES")
table_names = [row[2] for row in cur.fetchall()]

# Close the cursor and connection
cur.close()
conn.close()

# Display the snowflake details
st.write(f"Snowflake Account: {account}")
st.write(f"Username: {username}")

# Display the virtual warehouses dropdown
selected_warehouse = st.selectbox("Select virtual warehouse:", warehouse_names)

# Display the databases dropdown
selected_database = st.selectbox("Select database name:", database_names)

# Display the schemas dropdown
selected_schema = st.selectbox("Select schema name:", schema_names)

# Display the tables dropdown
selected_table = st.selectbox("Select table name:", table_names)

# Show the selected warehouse, database, schema, and table
st.write(f"Selected virtual warehouse: {selected_warehouse}")
st.write(f"Selected database: {selected_database}")
st.write(f"Selected schema: {selected_schema}")
st.write(f"Selected table: {selected_table}")
