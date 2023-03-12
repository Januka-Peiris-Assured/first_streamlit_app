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

            # Select role
            st.sidebar.header("Snowflake Roles")
            try:
                cursor.execute("SHOW ROLES")
                roles = [row[0] for row in cursor.fetchall()]
                role = st.sidebar.selectbox("Select a role", roles)
            except Exception as e:
                st.error("Error fetching roles: " + str(e))
                return

            try:
                cursor.execute(f"USE ROLE {role}")
            except Exception as e:
                st.error("Error selecting role: " + str(e))
                return

            # Select database and schema
            st.sidebar.header("Snowflake Databases")
            try:
                cursor.execute("SELECT name FROM INFORMATION_SCHEMA.DATABASES")
                databases = [row[0] for row in cursor.fetchall()]
                database = st.sidebar.selectbox("Select a database", databases)
            except Exception as e:
                st.error("Error fetching databases: " + str(e))
                return

            try:
                cursor.execute("USE DATABASE " + database)
            except Exception as e:
                st.error("Error selecting database: " + str(e))
                return

            st.sidebar.header("Snowflake Schemas")
            try:
                cursor.execute("SHOW SCHEMAS")
                schemas = [row[0] for row in cursor.fetchall()]
                schema = st.sidebar.selectbox("Select a schema", schemas)
            except Exception as e:
                st.error("Error fetching schemas: " + str(e))
                return

            try:
                cursor.execute("USE SCHEMA " + schema)
            except Exception as e:
                st.error("Error selecting schema: " + str(e))
                return

            # Show table information
            try:
                cursor.execute('SELECT * FROM information_schema.tables')
                tables = cursor.fetchall()
                st.write('### Tables in Snowflake:')
                for table in tables:
                    st.write('- ' + table.table_name)
            except Exception as e:
                st.error("Error fetching tables: " + str(e))

            # Show user information
            try:
                cursor.execute('SHOW USERS')
                users = cursor.fetchall()
                st.write('### Users in Snowflake:')
                for user in users:
                    st.write('- ' + user[0])
            except Exception as e:
                st.error("Error fetching users: " + str(e))

            # Show warehouse information
            try:
                cursor.execute('SHOW WAREHOUSES')
                warehouses = cursor.fetchall()
                st.write('### Warehouses in Snowflake:')
                for warehouse in warehouses:
                    st.write('- ' + warehouse[0])
            except Exception as e:
                st.error("Error fetching warehouses: " + str(e))
        else:
            return
