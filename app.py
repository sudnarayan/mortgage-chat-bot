# NOTE: This version does not use pandas and instead parses CSV manually.
# This script assumes that Streamlit and OpenAI libraries are available in the environment.

import os
import csv
import sys
import logging

# Setup logging for CLI fallback
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Check for dependencies
try:
    import streamlit as st
    import matplotlib.pyplot as plt
    from collections import Counter
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False

try:
    from openai import OpenAI
except ImportError:
    print("OpenAI module is not available. Please run: pip install openai")
    sys.exit(1)

# --- OpenAI Key ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not STREAMLIT_AVAILABLE:
    logging.warning("Streamlit is not available. This environment does not support CLI mode due to I/O restrictions.")
    sys.exit("This script must be run in a Streamlit-compatible environment.")

# --- Streamlit UI ---
st.set_page_config(page_title="Mortgage Insights Bot", layout="centered")
st.markdown("""
    <style>
    .main, .block-container {
        padding: 1.5rem;
    }
    .stTextInput > div > input {
        font-size: 16px;
    }
    .stButton > button {
        font-size: 16px;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Mortgage Insights Q&A Bot")

# --- Upload CSV ---
st.sidebar.header("Upload Your Mortgage Data (CSV)")
file = st.sidebar.file_uploader("Choose a file", type="csv")

if file:
    content = file.read().decode("utf-8")
    csv_lines = content.splitlines()
    reader = csv.reader(csv_lines)
    header = next(reader)
    rows = list(reader)

    st.subheader("🔍 Data Preview")
    st.dataframe([dict(zip(header, row)) for row in rows[:5]])

    # --- Filtering Option ---
    if "Status" in header:
        status_index = header.index("Status")
        unique_statuses = list(set(row[status_index] for row in rows))
        selected_status = st.sidebar.selectbox("Filter by Status", ["All"] + unique_statuses)

        if selected_status != "All":
            rows = [row for row in rows if row[status_index] == selected_status]

    # --- Basic Chart ---
    st.subheader("📈 Approval Status Chart")
    if "Status" in header:
        counts = Counter(row[header.index("Status")] for row in rows)
        fig, ax = plt.subplots()
        ax.bar(counts.keys(), counts.values())
        ax.set_title("Mortgage Application Status Distribution")
        st.pyplot(fig)

    # --- User Input ---
    st.subheader("💬 Ask a Question")
    query = st.text_input("What would you like to know about this data?")

    if query:
        # Convert a portion of the CSV to text context
        preview_text = "\n".join([", ".join(row) for row in [header] + rows[:100]])

        prompt = f"You are a financial data assistant. Here's a sample of a mortgage dataset:\n\n{preview_text}\n\nNow answer this question about the data:\n{query}"

        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You analyze mortgage data."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("Answer:")
                st.write(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Upload a CSV file to get started.")

