import streamlit as st
from streamlit_extras.let_it_rain import rain
import pandas as pd

st.set_page_config(page_title="Mortgage Insights Bot – Early Access", layout="centered")

st.title("🚀 Early Access Open: Mortgage Insights Bot")

st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a73e8;
        margin-bottom: 0.75rem;
        text-align: center;
    }
    .lead-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .footer-text {
        text-align: center; 
        margin-top: 2rem; 
        font-size: 0.9rem; 
        color: #777;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="lead-text">
We’re inviting 10 early users to test our AI-powered mortgage insights bot.<br>
Upload your CSV, ask questions, and get instant answers.<br>
Limited access — reserve your spot now!
</div>
""", unsafe_allow_html=True)

formsubmit_email = st.secrets["FORM_SUBMIT_EMAIL"]

st.markdown(f"""
<form action="https://formsubmit.co/{formsubmit_email}" method="POST">
    <input type="text" name="name" placeholder="Your Name" required style="width: 100%; padding: 10px; margin-bottom: 10px;">
    <input type="email" name="email" placeholder="Your Email" required style="width: 100%; padding: 10px; margin-bottom: 10px;">
    <textarea name="message" placeholder="What do you hope this bot can solve for you?" required style="width: 100%; padding: 10px; margin-bottom: 10px;"></textarea>
    <button type="submit" style="background-color: #1a73e8; color: white; padding: 10px 20px; border: none; border-radius: 5px;">Request Early Access</button>
</form>
""", unsafe_allow_html=True)

st.markdown("""
## 📄 Try Uploading Your Mortgage CSV
""")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(10))

    st.markdown("""
    ## 🧠 Quick AI Insight (MVP Feature!)
    """)
    st.info(f"This CSV contains {df.shape[0]} rows and {df.shape[1]} columns.")
    if 'loan_amount' in df.columns:
        st.success(f"Average Loan Amount: ${df['loan_amount'].mean():,.2f}")
    else:
        st.warning("Tip: Include a 'loan_amount' column to get more insights!")

st.markdown("""
<div class="footer-text">
Built by a solo maker. Feedback makes it better. 🛠️
</div>
""", unsafe_allow_html=True)

rain(emoji="🎯", font_size=24, falling_speed=5, animation_length="infinite")


