import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.connector import Error
from sqlalchemy import create_engine
import urllib.parse

st.set_page_config(page_title="Snowflake App")

# SNOWFLAKE CREDENTIALS
user = st.secrets["user"]
password = st.secrets["password"]
account = st.secrets["account"]
warehouse = st.secrets["warehouse"]
database = st.secrets["database"]
schema = st.secrets["schema"]

params = urllib.parse.quote_plus(
    f"account={account}&user={user}&password={password}&warehouse={warehouse}"
)
engine = create_engine(f"snowflake://{params}/DWH", pool_size=5)

# Connect to Snowflake
try:
    with snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
    ) as conn:
        st.sidebar.write(f"Connected to Snowflake: `{database}`.`{schema}`")
        # control tables
        dim_managers = pd.read_sql_query(
            f"SELECT * FROM DWH.CONTROL_TABLES.DIM_MANAGERS", conn
        )
        st.write(dim_managers)

        # Create a DataFrame
        data = {"name": ["John", "Paul", "George", "Ringo"], "age": [80, 78, 78, 81]}
        df = pd.DataFrame(data)

        # Display the DataFrame
        st.write(df)

        # Allow the user to edit the DataFrame
        st.write("Edit DataFrame")
        st.dataframe(df, editable=True)

        # Get the edited DataFrame
        edited_df = st.session_state.df
        new_table_name = st.text_input("Enter a new table name", "new_table")

        # Save changes to Snowflake table
        if st.button("Save changes"):
            # Update the "new" and "new_row" values to "changed"
            edited_df.loc[edited_df["_st_state"].isin(["new", "new_row"]), "_st_state"] = "changed"
            # Insert new rows
            new_rows = edited_df.loc[edited_df["_st_state"].isin(["new", "new_row"]), :]
            new_rows.to_sql(
                name=new_table_name,
                con=engine,
                schema=schema,
                index=False,
                if_exists="append",
            )
            # Update changed rows
            changed_rows = edited_df.loc[edited_df["_st_state"] == "changed", :]
            changed_rows.to_sql(
                name=new_table_name,
                con=engine,
                schema=schema,
                index=False,
                if_exists="append",
            )
            st.success("Changes saved to Snowflake!")
except Error as e:
    st.sidebar.error(f"Snowflake error occurred: {e}")
