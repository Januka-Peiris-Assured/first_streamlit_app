import snowflake.connector
import streamlit as st
import pandas as pd

# Create sidebar
with st.sidebar:
    st.write("### Login Details")
    account = st.text_input("Snowflake Account Name")
    user = st.text_input("User Name")
    password = st.text_input("Password", type="password")

# Connect to Snowflake
if st.button("Login"):
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


        st.write("Edit table")
        edited_df = st.experimental_data_editor(df, num_rows="dynamic") # 👈 An editable dataframe

        # Write back changes to Snowflake table
        # Save changes to Snowflake
    if st.button("Save Changes"):
        cursor.execute(f"SELECT * FROM {selected_database}.{selected_schema}.{selected_table}")
        data = cursor.fetchall()
        original_df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        edited_df = edited_df.astype(str)  # Convert all columns to str

        # Update existing rows
        for i, row in edited_df.iterrows():
            original_row = original_df.iloc[i]
            if not row.equals(original_row):
                set_values = ", ".join([f"{col} = '{row[col]}'" for col in row.index])
                where_clause = " AND ".join([f"{col} = '{original_row[col]}'" for col in row.index])
                update_query = f"UPDATE {selected_database}.{selected_schema}.{selected_table} SET {set_values} WHERE {where_clause}"
                cursor.execute(update_query)

        # Add new rows
        new_rows = edited_df.loc[edited_df["_st_state"].isin(["new", "new_row"]), :]
        if not new_rows.empty:
            new_rows.drop(columns=["_st_state"], inplace=True)
            new_rows.to_sql(name=selected_table, con=conn, schema=selected_schema, index=False, if_exists="append")

        st.write("Changes saved!")
