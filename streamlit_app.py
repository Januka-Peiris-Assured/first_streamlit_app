import snowflake.connector
import streamlit as st
import pandas as pd

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

# Select Snowflake role
cursor.execute("SELECT CURRENT_ROLE()")
current_role = cursor.fetchone()[0]
cursor.execute("SHOW ROLES")
roles = [row[1] for row in cursor.fetchall()]

selected_warehouse = st.selectbox("Virtual Warehouse", warehouses)
selected_role = st.selectbox("Role", roles, index=roles.index(current_role))

cursor.execute("USE ROLE {}".format(selected_role))

cursor.execute("SHOW DATABASES")
databases = [row[1] for row in cursor.fetchall()]

cursor.execute("SHOW SCHEMAS")
schemas = [row[1] for row in cursor.fetchall()]

# Display options for virtual warehouse, database, schema, and table
selected_database = st.selectbox("Database", databases)
selected_schema = st.selectbox("Schema", schemas)
cursor.execute(f"SHOW TABLES IN {selected_database}.{selected_schema}")
tables = [row[1] for row in cursor.fetchall()]
selected_table = st.selectbox("Table Name", tables)

# Retrieve table columns and preview data
def load_data():
    cursor.execute(f"SELECT * FROM {selected_database}.{selected_schema}.{selected_table} LIMIT 10")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
    return df

if selected_table:

    df = load_data()
    st.write(f"Columns: {', '.join(df.columns)}")
    st.write("Data Preview:")
    st.dataframe(df)

    edited_df = st.experimental_data_editor(df) # 👈 An editable dataframe
    favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
    st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
