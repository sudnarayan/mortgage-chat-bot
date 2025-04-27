import streamlit as st
import openai
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup OpenAI client
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Connect to Google Sheet
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    json_creds = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mortgage Leads").sheet1
    return sheet

# Send Thank You Email Function
def send_thank_you_email(to_email):
    sender_email = st.secrets["SENDER_EMAIL"]
    sender_password = st.secrets["SENDER_EMAIL_PASSWORD"]

    subject = "Thanks for Connecting with Mortgage Bot 🏡"
    body = f"""
    Hi there 👋,

    Thanks for connecting with us at Mortgage Chatbot (Canada)! 🇨🇦

    We're excited to help you with your mortgage questions and financing journey.
    Feel free to ask anything — we're here 24/7!

    Stay awesome,
    Mortgage Bot Team 🚀
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send Thank You email: {e}")
        return False

# Streamlit app config
st.set_page_config(page_title="🏠 Mortgage Chatbot (Streaming + Email Capture)", layout="wide")
st.title("🏠 Mortgage Chatbot (Streaming + Email Capture)")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "email_captured" not in st.session_state:
    st.session_state.email_captured = False
if "email_prompted" not in st.session_state:
    st.session_state.email_prompted = False

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

    # Stream Assistant Response
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

        # Handle Email Input Form
        if "**🎯 Would you like personalized mortgage tips?" in message["content"] and not st.session_state.email_captured:
            email = st.text_input("Enter your email address:", key="email_input")
            if email and "@" in email:
                st.success(f"Thanks! We've saved your email: {email}")
                st.session_state.email_captured = True

                try:
                    sheet = connect_to_sheet()
                    sheet.append_row([email, str(datetime.now())])
                    send_thank_you_email(email)
                except Exception as e:
                    st.error(f"Failed to save email or send Thank You email: {e}")

            elif email:
                st.warning("Please enter a valid email address.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by CSV Wizard")
