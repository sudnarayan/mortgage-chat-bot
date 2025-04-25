
import streamlit as st
from streamlit_extras.animated_headline import animated_headline
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="Mortgage Insights Bot – Early Access", layout="centered")

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
    .cta-button {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }
    .stButton button {
        background-color: #1a73e8;
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #1558b0;
    }
</style>
""", unsafe_allow_html=True)

animated_headline(
    "Early Access Open 🚀",
    ["Instant Mortgage Insights.", "Smarter Loan Decisions.", "Be the First to Know."]
)

st.markdown("""
<div class="lead-text">
We’re inviting 10 early users to test our AI-powered mortgage insights bot.<br>
Upload your CSV, ask questions, and get instant answers.<br>
Limited access — reserve your spot now!
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cta-button">
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSfuzQAKXWhTociKZ-cS-M0XPMVj_AQuNE7EMXwv7JTrb1mJTA/viewform?embedded=true" target="_blank">
        <button>Request Early Access</button>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
Built by a solo maker. Feedback makes it better. 🛠️
</div>
""", unsafe_allow_html=True)

rain(emoji="🎯", font_size=24, falling_speed=5, animation_length="infinite")
