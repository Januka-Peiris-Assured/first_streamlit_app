import snowflake.connector
import streamlit as st

# Get Snowflake account details from user input
account = st.text_input("Snowflake Account Name")
user = st.text_input("User Name")
password = st.text_input("Password", type="password")

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=account,
    user=user,
    password=password
)

# Retrieve list of virtual warehouses, databases, and schemas
cursor = conn.cursor()
cursor.execute("SHOW WAREHOUSES")
warehouses = [row[0] for row in cursor.fetchall()]

cursor.execute("SHOW DATABASES")
databases = [row[1] for row in cursor.fetchall()]

cursor.execute("SHOW SCHEMAS")
schemas = [row[1] for row in cursor.fetchall()]

# Display options for virtual warehouse, database, schema, and table
selected_warehouse = st.selectbox("Virtual Warehouse", warehouses)
selected_database = st.selectbox("Database", databases)
selected_schema = st.selectbox("Schema", schemas)
cursor.execute(f"SHOW TABLES IN {selected_database}.{selected_schema}")
tables = [row[1] for row in cursor.fetchall()]
selected_table = st.selectbox("Table Name", tables)

# Retrieve table columns and preview data
if selected_table:
    cursor.execute(f"DESCRIBE TABLE {selected_table}")
    columns = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"SELECT * FROM {selected_table} LIMIT 10")
    data = cursor.fetchall()

    st.write(f"Columns: {', '.join(columns)}")
    st.write("Data Preview:")
    st.write(data)
