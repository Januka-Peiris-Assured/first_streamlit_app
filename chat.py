import openai
import chatgpt
import snowflake.connector
import streamlit as st

openai.api_key = "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"



def run_query(query):
    # Connect to Snowflake
    cnx = snowflake.connector.connect(
        user='JanukaPE',
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

message = st.text_input("Enter your message:")
if message:
    response = chatbot_response(message)
    st.success(response)
