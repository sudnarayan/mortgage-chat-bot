import streamlit as st
import openai

# Streamlit page config
st.set_page_config(page_title="🏠 Mortgage Chatbot (GPT Powered)", layout="wide")

# Set up OpenAI client (NEW WAY - 2024 SDK)
client = openai.OpenAI(
    api_key=st.secrets.get("OPENAI_API_KEY")  # safer way
)

# Title
st.title("🏠 Mortgage Chatbot (GPT Powered)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get GPT response
def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful mortgage advisor. Keep answers simple, friendly, and Canada-focused."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500,
    )
    return response.choices[0].message.content

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about mortgages!"):
    # User message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = get_gpt_response(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by CSV Wizard")
