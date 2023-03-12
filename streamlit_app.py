import streamlit as st
import snowflake.connector as sf


# Connect to Snowflake
def connect_to_snowflake(user, password, account, warehouse):
    try:
        conn = sf.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
        )
        cursor = conn.cursor()
        return cursor
    except Exception as e:
        st.error("Error connecting to Snowflake: " + str(e))
        return None


# Main function
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
                cursor.execute(
                    'SELECT "name",  "owner", "comment" '
                    'FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));'
                )
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

            st.write(f"### Role selected: {role}")

            # User management
            st.write('## User Management')
            try:
                cursor.execute('SHOW USERS')
                users = cursor.fetchall()
                st.write('### Users in Snowflake:')
                for user in users:
                    st.write('- ' + user[0])
            except Exception as e:
                st.error("Error fetching users: " + str(e))

            # Database management
            st.write('## Database Management')
            try:
                cursor.execute("SELECT name FROM INFORMATION_SCHEMA.DATABASES")
                databases = [row[0] for row in cursor.fetchall()]
                database = st.selectbox("Select a database", databases)
            except Exception as e:
                st.error("Error fetching databases: " + str(e))
                return

            st.write(f"### Database selected: {database}")

            # Warehouse management
            st.write('## Warehouse Management')
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


if __name__ == "__main__":
    main()
