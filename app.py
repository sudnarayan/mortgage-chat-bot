import streamlit as st
import pandas as pd
import requests
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="Mortgage Insights Bot – Early Access", layout="centered")

st.markdown("""
<h1 style='text-align: center; font-size: 2.8rem; color: #1a73e8; margin-bottom: 1rem;'>🏠 Unlock Mortgage Insights Instantly</h1>
<p style='text-align: center; font-size: 1.2rem; color: #555;'>Upload your mortgage CSV. Get instant AI-powered insights. Make better decisions faster.</p>
<div style='text-align: center; margin-top: 2rem;'>
<a href="#form" style='background-color: #1a73e8; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-size: 1.1rem;'>🚀 Request Early Access Now</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .lead-text { font-size: 1.2rem; margin-bottom: 2rem; text-align: center; }
    .footer-text { text-align: center; margin-top: 2rem; font-size: 0.9rem; color: #777; }
    .pricing-table { display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; flex-wrap: wrap; }
    .pricing-card { background: #2c2f36; padding: 1.5rem; border-radius: 1rem; text-align: center; width: 250px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); color: white; }
    .price { font-size: 2rem; margin: 1rem 0; color: #4fc3f7; }
</style>
""", unsafe_allow_html=True)

rain(emoji="🎯", font_size=24, falling_speed=5, animation_length=30)

st.markdown("""
<div id="form" class="lead-text">
We’re inviting 10 early users to test our AI-powered mortgage insights bot.<br>
Upload your CSV, ask questions, and get instant answers.<br>
Limited access — reserve your spot now!
</div>
""", unsafe_allow_html=True)

formsubmit_email = st.secrets["FORM_SUBMIT_EMAIL"]
feedback_sheet_url = st.secrets["FEEDBACK_SHEET_WEBHOOK"]

st.markdown(f"""
<form action="https://formsubmit.co/{formsubmit_email}" method="POST">
    <input type="hidden" name="_autoresponse" value="Thanks for signing up for Mortgage Insights Bot Early Access! We will contact you shortly.">
    <input type="text" name="name" placeholder="Your Name" required style="width: 100%; padding: 10px; margin-bottom: 10px;'>
    <input type="email" name="email" placeholder="Your Email" required style="width: 100%; padding: 10px; margin-bottom: 10px;'>
    <textarea name="message" placeholder="What do you hope this bot can solve for you?" required style="width: 100%; padding: 10px; margin-bottom: 10px;'></textarea>
    <button type="submit" style="background-color: #1a73e8; color: white; padding: 10px 20px; border: none; border-radius: 5px;'>Request Early Access</button>
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
    ## 🧠 Quick Mortgage Insights
    """)
    st.info(f"This dataset contains {df.shape[0]} loans across {df.shape[1]} features.")

    if 'loan_amount' in df.columns:
        avg_loan = df['loan_amount'].mean()
        max_loan = df['loan_amount'].max()
        min_loan = df['loan_amount'].min()
        st.success(f"Average Loan Amount: ${avg_loan:,.2f}")
        st.success(f"Highest Loan Amount: ${max_loan:,.2f}")
        st.success(f"Lowest Loan Amount: ${min_loan:,.2f}")
    else:
        st.warning("Tip: Include a 'loan_amount' column to unlock full mortgage insights!")

    st.markdown("""
    ## ✨ We'd love your feedback!
    """)
    with st.form("feedback_form"):
        satisfaction = st.slider("How helpful were the insights?", 1, 5, 3)
        confusion = st.text_input("What confused you the most?")
        recommend = st.radio("Would you recommend us to others?", ["Yes", "No"])
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            feedback_data = {
                "Satisfaction": satisfaction,
                "Confusion": confusion,
                "Recommend": recommend
            }
            try:
                requests.post(feedback_sheet_url, json=feedback_data)
                st.success("🎉 Thanks for your feedback! We recorded it!")
            except:
                st.error("⚠️ Failed to send feedback. Please try again.")

rain(emoji="🎯", font_size=0)

st.markdown("""
## 💰 Early Access Pricing Plans
<div class="pricing-table">
    <div class="pricing-card">
        <h3>Starter</h3>
        <div class="price">$5/mo</div>
        <p>CSV Uploads</p>
        <p>Basic Mortgage Insights</p>
        <p>Email Support</p>
    </div>
    <div class="pricing-card">
        <h3>Pro</h3>
        <div class="price">$10/mo</div>
        <p>Advanced Risk Analysis</p>
        <p>Early Feature Access</p>
        <p>Priority Email Support</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
Built by a solo maker in 🇨🇦. Feedback makes it better. 🛠️
</div>
""", unsafe_allow_html=True)
