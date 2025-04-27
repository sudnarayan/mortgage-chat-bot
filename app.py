# Note: This environment does not support Streamlit. This code assumes running locally with Streamlit installed.

try:
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
    import json
    import google.auth.transport.requests
    from google.oauth2 import service_account
    import streamlit.components.v1 as components

    # --- SEO + Landing Page Head Injection ---
    st.set_page_config(
        page_title="Canadian Mortgage Chatbot | Get Expert Answers Fast",
        page_icon="🏠",
        layout="wide",
    )

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

    st.markdown("## Get Instant Answers to Your Canadian Mortgage Questions")

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

    client = openai.OpenAI(
        api_key=st.secrets.get("OPENAI_API_KEY", "fake-key-for-demo")
    )

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

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

    prompt = st.chat_input("Ask me anything about mortgages!")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        full_response = ""
        for chunk in stream_gpt_response(prompt):
            full_response += chunk
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    user_messages = [m for m in st.session_state.messages if m["role"] == "user"]

    if len(user_messages) == 3 and not st.session_state.email_captured and not st.session_state.email_prompted:
        with st.expander("🎯 Get personalized mortgage tips - Enter Email"):
            email = st.text_input("Enter your email address:", key="email_input_after_3")
            if email and "@" in email:
                st.success(f"Thanks! We've saved your email: {email}")
                st.session_state.email_captured = True
                st.session_state.user_email = email
                st.session_state.messages.append({"role": "assistant", "content": "Thank you for providing your email!"})
            elif email:
                st.warning("Please enter a valid email address.")
        st.session_state.email_prompted = True

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.email_captured:
        st.write(f"Your email: {st.session_state.user_email}")

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

    st.markdown("---")
    st.markdown("Built with ❤️ by CSV Wizard")

except ModuleNotFoundError as e:
    print("Required module not found. Please make sure Streamlit is installed and you are running this locally.")
    print(str(e))
