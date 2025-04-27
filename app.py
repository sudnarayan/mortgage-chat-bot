import streamlit as st
import pandas as pd

# Set the page title
st.set_page_config(page_title="CSV Uploader & Explorer")

st.title("📄 CSV File Uploader and Explorer")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        st.success("File successfully uploaded and read! ✅")

        # Display first 10 rows
        st.subheader("🔍 First 10 Rows of Your Data")
        st.dataframe(df.head(10))

        # Display column names
        st.subheader("🧩 Columns Available")
        st.write(list(df.columns))

        # Dropdown to select a column
        st.subheader("🎯 Explore Unique Values")
        selected_column = st.selectbox("Pick a column to see its unique values", df.columns)

        if selected_column:
            unique_values = df[selected_column].unique()
            st.write(f"Unique values in **{selected_column}**:", unique_values)

    except Exception as e:
        st.error(f"❌ Error reading the CSV file: {e}")
else:
    st.info("Please upload a CSV file to get started.")
