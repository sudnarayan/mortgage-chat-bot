import streamlit as st
import pandas as pd
import plotly.express as px
import os
import uuid

# Set page config
st.set_page_config(page_title="CSV Wizard", page_icon="📄", layout="wide")

st.title("📄 CSV Wizard - Upload, Analyze & Transform Your Data")
st.markdown("A simple but powerful app to explore CSV files easily.")

# Upload directory setup
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Upload & Display",
    "Filter Data",
    "Summary Statistics",
    "Scatter Plot",
    "Create New Column",
    "Download Data",
    "Data Validation"
])

# File uploader
st.sidebar.subheader("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV", type=["csv"])

# If file is uploaded
if uploaded_file:
    try:
        delimiter = st.sidebar.text_input("CSV Delimiter (default is ',')", value=",")
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
        
        # Save uploaded file
        file_id = uuid.uuid4().hex
        save_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.sidebar.success(f"File saved at {save_path}")
        
        if page == "Upload & Display":
            st.subheader("First 5 Rows")
            st.dataframe(df.head())
            st.subheader("Columns and Data Types")
            st.write(df.dtypes)
        
        elif page == "Filter Data":
            st.subheader("Filter Data by Column Value")
            column = st.selectbox("Select Column", df.columns)
            if column:
                value = st.selectbox("Select Value", df[column].dropna().unique())
                filtered_df = df[df[column] == value]
                st.dataframe(filtered_df)
        
        elif page == "Summary Statistics":
            st.subheader("Summary Statistics")
            num_cols = st.multiselect("Select Numerical Columns", df.select_dtypes(include=['float64', 'int64']).columns)
            if num_cols:
                st.write("Mean:", df[num_cols].mean())
                st.write("Median:", df[num_cols].median())
                st.write("Standard Deviation:", df[num_cols].std())
        
        elif page == "Scatter Plot":
            st.subheader("Scatter Plot")
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            x_axis = st.selectbox("Select X Axis", numeric_cols)
            y_axis = st.selectbox("Select Y Axis", numeric_cols)
            if x_axis and y_axis:
                fig = px.scatter(df, x=x_axis, y=y_axis)
                st.plotly_chart(fig)
        
        elif page == "Create New Column":
            st.subheader("Create New Column with Formula")
            st.markdown("Example formula: `Price * Quantity`")
            formula = st.text_input("Enter your formula here")
            if formula:
                try:
                    df["New_Column"] = df.eval(formula)
                    st.success("New column created successfully!")
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"Error applying formula: {e}")
        
        elif page == "Download Data":
            st.subheader("Download Modified Data")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="modified_data.csv",
                mime="text/csv",
            )
        
        elif page == "Data Validation":
            st.subheader("Validate Column Data Types")
            st.markdown("Enter expected types like: `{ 'Age': 'int', 'Name': 'str' }`")
            expected_types = st.text_input("Expected Types (as Python dictionary)")
            if expected_types:
                try:
                    expected_types_dict = eval(expected_types)
                    mismatches = {}
                    for col, expected_type in expected_types_dict.items():
                        if col in df.columns:
                            actual_type = df[col].dtype
                            if expected_type == 'int' and not pd.api.types.is_integer_dtype(df[col]):
                                mismatches[col] = str(actual_type)
                            elif expected_type == 'float' and not pd.api.types.is_float_dtype(df[col]):
                                mismatches[col] = str(actual_type)
                            elif expected_type == 'str' and not pd.api.types.is_string_dtype(df[col]):
                                mismatches[col] = str(actual_type)
                        else:
                            mismatches[col] = "Column missing"
                    if mismatches:
                        st.error(f"Mismatches found: {mismatches}")
                    else:
                        st.success("All columns match expected types!")
                except Exception as e:
                    st.error(f"Invalid input: {e}")
        
    except Exception as e:
        st.error(f"Failed to read the CSV file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
