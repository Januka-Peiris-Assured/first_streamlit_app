import streamlit as st
import snowflake.connector as sf

def connect_to_snowflake(user, password, account, warehouse):
    try:
        conn = sf.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
        )
        return conn.cursor()
    except Exception as e:
        st.error("Error connecting to Snowflake: " + str(e))
        return None

def main():
    st.sidebar.title("Snowflake Admin Tool")

    # Get Snowflake credentials from user
    st.sidebar.header("Snowflake Credentials")
    user = st.sidebar.text_input("User")
    password = st.sidebar.text_input("Password", type="password")
    account = st.sidebar.text_input("Account")
    warehouse = st.sidebar.text_input("Warehouse")

    # Connect to Snowflake
    if st.sidebar.button("Connect"):
        cursor = connect_to_snowflake(user, password, account, warehouse)
        if cursor:
            st.success("Connected to Snowflake!")

            # Select database and schema
            st.sidebar.header("Snowflake Databases")
            cursor.execute("SHOW DATABASES")
            databases = [row[0] for row in cursor.fetchall()]
            database = st.sidebar.selectbox("Select a database", databases)

            cursor.execute("USE DATABASE " + database)

            st.sidebar.header("Snowflake Schemas")
            cursor.execute("SHOW SCHEMAS")
            schemas = [row[0] for row in cursor.fetchall()]
            schema = st.sidebar.selectbox("Select a schema", schemas)

            cursor.execute("USE SCHEMA " + schema)

            # Show table information
            cursor.execute('SELECT * FROM information_schema.tables')
            tables = cursor.fetchall()
            st.write('### Tables in Snowflake:')
            for table in tables:
                st.write('- ' + table.table_name)

            # Show user information
            cursor.execute('SHOW USERS')
            users = cursor.fetchall()
            st.write('### Users in Snowflake:')
            for user in users:
                st.write('- ' + user[0])

            # Show role information
            cursor.execute('SHOW ROLES')
            roles = cursor.fetchall()
            st.write('### Roles in Snowflake:')
            for role in roles:
                st.write('- ' + role[0])

            # Show warehouse information
            cursor.execute('SHOW WAREHOUSES')
            warehouses = cursor.fetchall()
            st.write('### Warehouses in Snowflake:')
            for warehouse in warehouses:
                st.write('- ' + warehouse[0])
        else:
            return

if __name__ == '__main__':
    main()
