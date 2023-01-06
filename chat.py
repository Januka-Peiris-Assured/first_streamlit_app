import streamlit as st
import snowflake.connector

def run_query(query):
    # Connect to Snowflake
    cnx = snowflake.connector.connect(
        user='JanukaPe',
        password='Lavern1990!',
        account='sh69458.ca-central-1.aws'
    )

    # Create a cursor
    cursor = cnx.cursor()

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    result = cursor.fetchall()

    # Close the connection
    cnx.close()

    return result

def chatbot_response(input):
    # Use ChatGPT to generate a response
    response = chatgpt.get_response(input)

    # If the response includes a Snowflake query, execute it
    if "snowflake" in response.lower():
        result = run_query(response)
        return "Here are the results of your query: {}".format(result)
    else:
        return response

st.title("Chatbot")

input = st.text_input("Enter your message:")

if input:
    response = chatbot_response(input)
    st.write(response)
