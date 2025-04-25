
import streamlit as st

st.set_page_config(page_title="Mortgage Insights Bot – Early Access", layout="centered")

st.markdown("""
<style>
    .big-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 0.5rem;
    }
    .lead-text {
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    iframe {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-title">🚀 Get Early Access to Mortgage Insights Bot</div>
<p class="lead-text">
We’re inviting 10 early users to test our AI-powered mortgage insights bot.<br>
Upload your CSV, ask questions, and get instant answers.
</p>
""", unsafe_allow_html=True)

# 🔗 Embed updated working Google Form — ⚠️ Double-check that this is the exact same form that's connected to your Google Sheet and collecting responses — otherwise the response count in the Form UI may show zero.
st.components.v1.html("""
<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfuzQAKXWhTociKZ-cS-M0XPMVj_AQuNE7EMXwv7JTrb1mJTA/viewform?embedded=true" 
        width="700" height="900" frameborder="0" marginheight="0" marginwidth="0">
Loading…
</iframe>
<p style='text-align: center; font-size: 1rem; margin-top: 1rem; color: green;'>✅ Thank you for submitting! Check your email for early access info.</p>
""", height=1000)

st.markdown("""
<div style="text-align:center; margin-top: 2rem; font-size: 0.9rem; color: #777;">
Built by a solo maker. Feedback makes it better. 🛠️
</div>
""", unsafe_allow_html=True)
