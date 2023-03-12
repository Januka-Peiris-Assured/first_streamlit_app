import streamlit as st
import snowflake.connector as sf
import pandas as pd


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
                    'SHOW ROLES'
                )
                roles = [row[0] for row in cursor.fetchall()]
                role = st.sidebar.selectbox("Select a role", roles)
                cursor.execute(f'USE ROLE "{role}"')
            except Exception as e:
                st.error("Error fetching or selecting role: " + str(e))
                return

            st.write(f"### Role selected: {role}")

            # User management
            st.write('## User Management')
            try:
                cursor.execute('SHOW USERS')
                users = cursor.fetchall()
                df_users = pd.DataFrame(users, columns=['User', 'Created On', 'Default Namespace'])
                st.dataframe(df_users, use_container_width=True)
            except Exception as e:
                st.error("Error fetching users: " + str(e))

            # Warehouse management
            st.write('## Warehouse Management')
            try:
                cursor.execute('SHOW WAREHOUSES')
                warehouses = cursor.fetchall()
                df_warehouses = pd.DataFrame(warehouses, columns=['Warehouse', 'State', 'Size', 'AutoSuspend', 'Created On', 'Retained For'])
                st.dataframe(df_warehouses, use_container_width=True)
            except Exception as e:
                st.error("Error fetching warehouses: " + str(e))

        else:
            return


if __name__ == "__main__":
    main()
