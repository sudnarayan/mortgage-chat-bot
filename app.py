import streamlit as st
import openai
import gspread
import json
from io import StringIO
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup OpenAI client
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Setup Google Sheets connection using Streamlit Secrets
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    json_creds = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mortgage Leads").sheet1
    return sheet

# Streamlit page setup
st.set_page_config(page_title="🏠 Mortgage Chatbot (Streaming + Email Capture)", layout="wide")
st.title("🏠 Mortgage Chatbot (Streaming + Email Capture)")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "email_captured" not in st.session_state:
    st.session_state.email_captured = False
if "email_prompted" not in st.session_state:
    st.session_state.email_prompted = False

# GPT streaming response function
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

# Chat input handling
if prompt := st.chat_input("Ask me anything about mortgages!"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream the assistant response
    full_response = ""
    for chunk in stream_gpt_response(prompt):
        full_response += chunk
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Count user messages separately
user_messages = [m for m in st.session_state.messages if m["role"] == "user"]

# 👇 Inject Email Capture inside the chat flow
if len(user_messages) == 3 and not st.session_state.email_captured and not st.session_state.email_prompted:
    st.session_state.messages.append({"role": "assistant", "content": "**🎯 Would you like personalized mortgage tips? Enter your email below!**"})
    st.session_state.email_prompted = True

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # 👇 If it's the special email prompt, show input inside chat
        if "**🎯 Would you like personalized mortgage tips?" in message["content"] and not st.session_state.email_captured:
            email = st.text_input("Enter your email address:", key="email_input")
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

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by CSV Wizard")
