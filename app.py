import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mortgage Insights Bot", layout="wide")

# Store user email for private access (in session state for demo purposes)
if "email" not in st.session_state:
    st.session_state.email = ""
if "email_list" not in st.session_state:
    st.session_state.email_list = []

# Onboarding Header
st.markdown("""
# 👋 Welcome to Mortgage Insights Bot

Get powerful insights from your mortgage data using AI. 

### 🧪 We're currently onboarding 10 early users.
Fill the form below to join the beta and get priority access!
""")

# Email Capture
email_input = st.text_input("📨 Enter your email to preview the bot")
if email_input and "@" in email_input:
    st.session_state.email = email_input
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.email_list.append({"email": email_input, "timestamp": timestamp})
    st.success("✅ You're on the access list! Check your inbox for confirmation soon.")

# Export email list as CSV button (visible only if there is data)
if st.session_state.email_list:
    export_df = pd.DataFrame(st.session_state.email_list)
    csv = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Captured Emails (CSV)", csv, "early_access_emails.csv", "text/csv")

# Gated Premium Content (visible only if email is captured)
if st.session_state.email:
    st.markdown("""
    ---
    ## 🔍 Live Demo: Upload Mortgage Data
    Upload a sample CSV file to see how the bot works.
    """)
    uploaded_file = st.file_uploader("Upload your mortgage CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Here's a preview of your data:")
        st.dataframe(df.head())
        st.info("Imagine now asking: 'What’s the average loan amount for denied applicants?' ✨")
else:
    st.warning("🔒 Please enter your email above to unlock the demo.")

# Two-column layout for the landing form
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <iframe 
      src="https://sudnarayan.github.io/mortgage-chat-bot/" 
      width="100%" 
      height="1000" 
      frameborder="0" 
      style="border: none;">
    </iframe>
    """, unsafe_allow_html=True)

with col2:
    st.success("💡 Why Join Early?")
    st.markdown("""
    - Instant answers from your mortgage data
    - No spreadsheets, no code
    - Built for advisors, underwriters, analysts

    ✅ Only 10 testers in this phase
    📬 You'll be notified first when full access is live
    """)

st.divider()
st.markdown("Want to skip the form? Email me: [sudnarayan@hotmail.com](mailto:sudnarayan@hotmail.com)")
