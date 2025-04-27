import streamlit as st
import openai
import pandas as pd
import plotly.express as px
import os
import uuid

# Set page config
st.set_page_config(page_title="🏠 Mortgage Chatbot - GPT Enhanced", layout="wide")

# Set your OpenAI API Key securely
openai.api_key = st.secrets.get("OPENAI_API_KEY")  # safer way
# or uncomment to hardcode (NOT recommended for production)
# openai.api_key = "your-actual-api-key-here"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate GPT-based response
def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful mortgage expert chatbot. Answer questions simply and clearly."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,  # controls creativity
        max_tokens=500,  # max length of reply
    )
    return response['choices'][0]['message']['content']

# Display chat history
st.title("🏠 Mortgage Chatbot (GPT Powered)")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
if prompt := st.chat_input("Ask me anything about mortgages!"):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate assistant message
    response = get_gpt_response(prompt)
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
