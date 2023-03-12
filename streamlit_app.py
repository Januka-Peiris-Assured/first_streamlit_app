import streamlit as st
import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('test.db')
        print(f'successful connection: {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)

    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print('Query executed successfully')
    except sqlite3.Error as e:
        print(f'Error executing query: {e}')

def create_table(conn):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        );
    '''
    execute_query(conn, create_table_query)

def insert_data(conn):
    insert_data_query = '''
        INSERT INTO customers (first_name, last_name, email)
        VALUES
            ('John', 'Doe', 'john.doe@email.com'),
            ('Jane', 'Doe', 'jane.doe@email.com')
    '''
    execute_query(conn, insert_data_query)

def select_all(conn):
    select_all_query = '''
        SELECT * FROM customers;
    '''
    cursor = conn.cursor()
    cursor.execute(select_all_query)
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    return rows, headers

def main():
    st.title('Test SQLite Database')

    conn = create_connection()
    if conn is not None:
        create_table(conn)
        insert_data(conn)
        rows, headers = select_all(conn)

        st.write('### Data in Streamlit DataFrame')
        st.dataframe(rows, headers=headers)
        
    else:
        st.write('Error creating database connection')

if __name__ == '__main__':
    main()
