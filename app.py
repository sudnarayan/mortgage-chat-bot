import streamlit as st
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup OpenAI client
client = openai.OpenAI(
    api_key=st.secrets.get("OPENAI_API_KEY")
)

# Setup Google Sheets client
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(".streamlit/streamlit-csvwizard-bot.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mortgage Leads").sheet1  # your sheet name
    return sheet

# Streamlit page setup
st.set_page_config(page_title="🏠 Mortgage Chatbot (GPT + Email Capture)", layout="wide")
st.title("🏠 Mortgage Chatbot (Streaming + Email Capture)")

# Session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "email_captured" not in st.session_state:
    st.session_state.email_captured = False
if "email_prompted" not in st.session_state:
    st.session_state.email_prompted = False

# GPT Streaming function
def stream_gpt_response(prompt):
    full_response = ""
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly mortgage expert. Keep it simple and Canadian-focused."},
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

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about mortgages!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_stream = stream_gpt_response(prompt)
        full_response = st.write_stream(response_stream)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 👇 Email Capture Logic
if len(st.session_state.messages) >= 6 and not st.session_state.email_captured and not st.session_state.email_prompted:
    with st.expander("🎯 Get personalized mortgage tips! (Optional)"):
        email = st.text_input("Enter your email:", key="email_input")
        if email and "@" in email:
            st.success(f"Thanks! We've saved your email: {email}")
            st.session_state.email_captured = True

            try:
                sheet = connect_to_sheet()
                sheet.append_row([email, str(datetime.now())])
            except Exception as e:
                st.error(f"Failed to save email: {e}")

        elif email:
            st.warning("Please enter a valid email address.")
    
    st.session_state.email_prompted = True  # Only ask once

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by CSV Wizard")
