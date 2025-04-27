import streamlit as st

# MUST be the very first Streamlit command
st.set_page_config(
    page_title="Canadian Mortgage Chatbot | Get Expert Answers Fast",
    page_icon="🏠",
    layout="wide",
)

import openai
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import google.auth.transport.requests
from google.oauth2 import service_account
import streamlit.components.v1 as components

# --- SEO + Landing Page Head Injection ---
components.html(
    """
    <head>
        <title>Mortgage Chatbot Canada - Free Mortgage Help 24/7</title>
        <meta name="description" content="Talk to Canada's smartest Mortgage Chatbot. Free advice, simple guidance, available 24/7! Get mortgage answers instantly.">
        <meta name="keywords" content="Mortgage Chatbot Canada, Mortgage Help, Home Loans Canada, Mortgage Rates, Mortgage Questions, Mortgage Tips, Mortgage Chat Assistant, Streamlit Mortgage Bot">
        <meta name="author" content="CSV Wizard">
    </head>
    """,
    height=0,
)

# SEO: Main heading with relevant keywords
st.title("🏠 Mortgage Chatbot (Canada) - Your AI-Powered Mortgage Expert")

# SEO: Subheading with keyword variation
st.markdown("## Get Instant Answers to Your Canadian Mortgage Questions")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "email_captured" not in st.session_state:
    st.session_state.email_captured = False
if "email_prompted" not in st.session_state:
    st.session_state.email_prompted = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "credentials" not in st.session_state:
    st.session_state.credentials = None

# Setup OpenAI client
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# --- OAuth 2.0 Setup for Google Sheets ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_PATH = "token.json"

# Credentials functions...
# [Keep your existing get_credentials_oauth(), connect_to_sheet(), send_thank_you_email() here unchanged]

# Streaming GPT response function
def stream_gpt_response(prompt):
    full_response = ""
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly mortgage expert focused on Canadian mortgage advice."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content
    return full_response

# Chat Input Handling
if prompt := st.chat_input("Ask me anything about mortgages!"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    full_response = ""
    for chunk in stream_gpt_response(prompt):
        full_response += chunk
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Check if user needs to be asked for Email
user_messages = [m for m in st.session_state.messages if m["role"] == "user"]

if len(user_messages) == 3 and not st.session_state.email_captured and not st.session_state.email_prompted:
    st.session_state.messages.append({"role": "assistant", "content": "**🎯 Would you like personalized mortgage tips? Enter your email below!**"})
    st.session_state.email_prompted = True

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if "**🎯 Would you like personalized mortgage tips?" in message["content"] and not st.session_state.email_captured:
            email = st.text_input("Enter your email address:", key="email_input")
            if email and "@" in email:
                st.success(f"Thanks! We've saved your email: {email}")
                st.session_state.email_captured = True
                st.session_state.user_email = email

                creds = get_credentials_oauth()
                if creds:
                    sheet = connect_to_sheet(creds)
                    if sheet:
                        try:
                            sheet_id = "17CITdwS0z4Lhzl-ZPVCe0Dwukl1fQan2z1gnhabVSpI"
                            sheet.values().append(spreadsheetId=sheet_id, range='Sheet1', valueInputOption='RAW', body={'values': [[email, str(datetime.now())]]}).execute()
                            send_thank_you_email(email)
                        except Exception as e:
                            st.error(f"Failed to save email or send Thank You email: {e}")
                    else:
                        st.error("Failed to connect to Google Sheets using OAuth.")
                else:
                    st.error("Failed to obtain Google credentials using OAuth.")

                st.session_state.messages.append({"role": "assistant", "content": "Thank you for providing your email!"})
            elif email:
                st.warning("Please enter a valid email address.")

# Display email after capture
if st.session_state.email_captured:
    st.write(f"Your email: {st.session_state.user_email}")

# SEO: Add more details about chatbot
st.markdown("""
## About Our Mortgage Chatbot

Our AI-powered chatbot provides fast, accurate answers to your Canadian mortgage questions. We cover:
- Mortgage rates and calculations
- Pre-approval and qualification
- Refinancing options
- Mortgage terms and conditions
- Canadian mortgage regulations

We're here to simplify your journey. Ask us anything!
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by CSV Wizard")
