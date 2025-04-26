import streamlit as st
from streamlit_extras.let_it_rain import rain
import pandas as pd

st.set_page_config(page_title="Mortgage Insights Bot – Early Access", layout="centered")

st.markdown("""
<h1 style='text-align: center; font-size: 2.5rem; color: #1a73e8; margin-bottom: 1rem;'>
🚀 Mortgage Insights Bot – Early Access
</h1>
""", unsafe_allow_html=True)

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
    .pricing-table {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    .pricing-card {
        background: #2c2f36;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        width: 250px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        color: white;
    }
    .price {
        font-size: 2rem;
        margin: 1rem 0;
        color: #4fc3f7;
    }
</style>
""", unsafe_allow_html=True)

rain(emoji="🎯", font_size=24, falling_speed=5, animation_length=30)

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
    <input type="hidden" name="_autoresponse" value="Thanks for signing up for Mortgage Insights Bot Early Access! We will contact you shortly.">
    <input type="text" name="name" placeholder="Your Name" required style="width: 100%; padding: 10px; margin-bottom: 10px;">
    <input type="email" name="email" placeholder="Your Email" required style="width: 100%; padding: 10px; margin-bottom: 10px;">
    <textarea name="message" placeholder="What do you hope this bot can solve for you?" required style="width: 100%; padding: 10px; margin-bottom: 10px;"></textarea>
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
Built by a solo maker. Feedback makes it better. 🛠️
</div>
""", unsafe_allow_html=True)
