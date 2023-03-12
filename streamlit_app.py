# Set default values
database = ""
schema = ""

# Connect to Snowflake
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

    # Select database and schema
    cursor.execute("SHOW DATABASES")
    databases = [row[0] for row in cursor.fetchall()]
    database = st.sidebar.selectbox("Select a database", databases)

    cursor.execute("USE DATABASE " + database)

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
