import streamlit as st
import openai
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json  # Import the json module
import google.auth.transport.requests  # Import for making requests
from google.oauth2 import service_account # Import service account

# Setup OpenAI client
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# --- OAuth 2.0 for Google Sheets ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]  # Added drive.file scope
CLIENT_SECRET_FILE = "client_secret.json"  # Name of your client secret file
TOKEN_PATH = "token.json"

def get_credentials_oauth():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(google.auth.transport.requests.Request())
            except Exception as e:
                st.error(f"Error refreshing credentials: {e}")
                os.remove(TOKEN_PATH)  # Remove the invalid token file
                creds = None  # Force re-authorization
        if not creds:
            #  Use json.loads to parse the service account info, and write to client_secret.json
            client_secret_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
            # Check the type of client.  If it is a service account, use service account.
            if client_secret_info['type'] == 'service_account':
                try:
                    creds = service_account.Credentials.from_service_account_info(client_secret_info, scopes=SCOPES)
                except Exception as e:
                    st.error(f"Error creating service account credentials: {e}")
                    return None
            else: # Else use InstalledAppFlow
                with open(CLIENT_SECRET_FILE, 'w') as f:
                    json.dump(client_secret_info, f, indent=4) #indent for readability
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                flow.redirect_uri = "http://localhost:8501"  # Or your Streamlit Cloud URL - important for the auth flow
                auth_url, _ = flow.authorization_url()
                st.session_state.auth_url = auth_url #save auth url to session
                st.write(f'Please go to this URL to authorize: {auth_url}')
                code = st.text_input("Enter the authorization code:")
                if code:
                    try:
                        token_response = flow.fetch_token(code=code)
                        creds = flow.credentials
                        with open(TOKEN_PATH, 'w') as token:
                            token.write(creds.to_json())
                        st.session_state.credentials = creds
                    except Exception as e:
                        st.error(f"Error fetching token: {e}")
                        return None
                else:
                    return None #Stop if code is not provided
    return creds

def connect_to_sheet(creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        return sheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# --- End OAuth 2.0 ---

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
# SEO: Set a more descriptive page title
st.set_page_config(
    page_title="Canadian Mortgage Chatbot | Get Expert Answers Fast",
    page_icon="🏠",  # You can use an emoji or a URL to a favicon
    layout="wide",
    # SEO: Add meta description for search engine snippets
    description="Get instant answers to your Canadian mortgage questions with our AI-powered chatbot.  Ask about rates, qualifications, refinancing, and more.  Serving all of Canada.",
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
if "user_email" not in st.session_state:  # Store user email
    st.session_state.user_email = ""
if "credentials" not in st.session_state:
    st.session_state.credentials = None

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
                st.session_state.user_email = email  # Store the email

                #  Use OAuth to connect to Google Sheets and append the row.
                creds = get_credentials_oauth()
                if creds:
                    sheet = connect_to_sheet(creds)
                    if sheet:
                        try:
                            # Use the sheet ID from the provided URL
                            sheet_id = "17CITdwS0z4Lhzl-ZPVCe0Dwukl1fQan2z1gnhabVSpI"
                            sheet.values().append(spreadsheetId=sheet_id, range='Sheet1', valueInputOption='RAW', body={'values': [[email, str(datetime.now())]]}).execute()
                            send_thank_you_email(email)
                        except Exception as e:
                            st.error(f"Failed to save email: {e}")
                    else:
                        st.error("Failed to connect to Google Sheets using OAuth.")
                else:
                    st.error("Failed to obtain Google credentials using OAuth.")
                st.session_state.messages.append({"role": "assistant", "content": "Thank you for providing your email!"})

            elif email:
                st.warning("Please enter a valid email address.")

# Display email only after it has been captured
if st.session_state.email_captured:
    st.write(f"Your email: {st.session_state.user_email}")

# SEO: Add a section with more details about the chatbot
st.markdown("""
## About Our Mortgage Chatbot

Our AI-powered chatbot is designed to provide you with fast, accurate answers to your Canadian mortgage questions.  Whether you're a first-time homebuyer or looking to refinance, we can help.  We cover a wide range of topics, including:

* Mortgage rates and calculations
* Pre-approval and qualification requirements
* Refinancing options
* Mortgage terms and conditions
* Canadian mortgage regulations

We're here to help you navigate the complexities of the Canadian mortgage market.  Ask us anything!
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by CSV Wizard")
