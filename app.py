import streamlit as st
import openai

# Setup OpenAI client
client = openai.OpenAI(
    api_key=st.secrets.get("OPENAI_API_KEY")
)

# Page Config
st.set_page_config(page_title="🏠 Mortgage Chatbot (Streaming GPT)", layout="wide")

# Title
st.title("🏠 Mortgage Chatbot (Streaming GPT Powered)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# GPT response generator with streaming
def stream_gpt_response(prompt):
    full_response = ""
    # Create the stream
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly mortgage expert. Answer simply, based on Canadian rules."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500,
        stream=True  # <-- KEY for streaming
    )

    # Stream each chunk/token
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content  # Stream out token-by-token
    return full_response

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask me anything about mortgages!"):
    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream Assistant Response
    with st.chat_message("assistant"):
        response_stream = stream_gpt_response(prompt)
        full_response = st.write_stream(response_stream)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by CSV Wizard")
