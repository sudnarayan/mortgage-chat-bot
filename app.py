import streamlit as st
import streamlit.components.v1 as components

# Inject SEO Meta manually
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

# Correct page config
st.set_page_config(
    page_title="Mortgage Chatbot Canada - Free Mortgage Help 24/7",
    page_icon="🏡",
    layout="wide"
)
