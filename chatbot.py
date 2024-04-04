from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

# Function to get Gemini's response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Chatbot", page_icon=":robot_face:", layout="wide", initial_sidebar_state="collapsed")

# Set white theme
st.markdown(
"""
<style>
    body {
        color: black;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field for queries
input_text = st.text_input("Query:", key="input")

# Button to submit query
submit_button = st.button("Ask")

# Button to view chat history
history_button = st.button("History")

if submit_button and input_text:
    # Get response from Gemini
    response = get_gemini_response(input_text)
    st.subheader("Answer for your query:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("You", input_text))
        st.session_state['chat_history'].append(("Bot", chunk.text))

if history_button:
    st.subheader("Your Chat History:") 
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
