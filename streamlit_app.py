import snowflake.connector as sf

def connect_to_snowflake():
    conn = sf.connect(
        user='<your_user>',
        password='<your_password>',
        account='<your_account>',
        warehouse='<your_warehouse>',
        database='<your_database>',
        schema='<your_schema>'
    )

    return conn.cursor()


import streamlit as st

def main():
    st.sidebar.title("Snowflake Admin Tool")
    options = ['Tables', 'Users', 'Roles', 'Warehouses']
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == 'Tables':
        cursor = connect_to_snowflake()
        cursor.execute('SELECT * FROM information_schema.tables')
        tables = cursor.fetchall()
        st.write('### Tables in Snowflake:')
        for table in tables:
            st.write('- ' + table.table_name)

    elif choice == 'Users':
        cursor = connect_to_snowflake()
        cursor.execute('SHOW USERS')
        users = cursor.fetchall()
        st.write('### Users in Snowflake:')
        for user in users:
            st.write('- ' + user[0])

    elif choice == 'Roles':
        cursor = connect_to_snowflake()
        cursor.execute('SHOW ROLES')
        roles = cursor.fetchall()
        st.write('### Roles in Snowflake:')
        for role in roles:
            st.write('- ' + role[0])

    elif choice == 'Warehouses':
        cursor = connect_to_snowflake()
        cursor.execute('SHOW WAREHOUSES')
        warehouses = cursor.fetchall()
        st.write('### Warehouses in Snowflake:')
        for warehouse in warehouses:
            st.write('- ' + warehouse[0])

if __name__ == '__main__':
    main()
