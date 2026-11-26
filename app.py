import streamlit as st
import pandas as pd

# -------------------------------
# Page settings
# -------------------------------
st.set_page_config(
    page_title="AI Data Cleaner",
    page_icon="🧹",
    layout="wide"
)

# App title
st.title("🧹 AI Data Cleaner")

st.write("Upload your CSV or Excel file and clean your data.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader(
    "📁 Upload your dataset",
    type=["csv", "xlsx"]
)

# Continue only when a file is uploaded
if uploaded_file is not None:

    # Read CSV
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)

    # Read Excel
    else:
        data = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")

    # -------------------------------
    # Dataset Information
    # -------------------------------
    st.subheader("📊 Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", data.shape[0])
    col2.metric("Columns", data.shape[1])
    col3.metric("Duplicate Rows", data.duplicated().sum())

    # -------------------------------
    # Data Preview
    # -------------------------------
    st.subheader("👀 Data Preview")

    st.dataframe(data, use_container_width=True)

    # -------------------------------
    # Missing Values
    # -------------------------------
    st.subheader("❌ Missing Values")

    missing_values = data.isnull().sum()

    st.dataframe(
        missing_values[missing_values > 0]
    )

    # -------------------------------
    # Cleaning Options
    # -------------------------------
    st.subheader("🧹 Clean Your Data")

    cleaning_option = st.selectbox(
        "Choose a cleaning operation",
        [
            "None",
            "Remove Duplicate Rows",
            "Fill Missing Values"
        ]
    )

    # Remove duplicates
    if cleaning_option == "Remove Duplicate Rows":

        data = data.drop_duplicates()

        st.success("✅ Duplicate rows removed!")

    # Fill missing values
    elif cleaning_option == "Fill Missing Values":

        numeric_columns = data.select_dtypes(
            include="number"
        ).columns

        data[numeric_columns] = data[numeric_columns].fillna(
            data[numeric_columns].median()
        )

        st.success(
            "✅ Missing numerical values filled with median!"
        )

    # -------------------------------
    # Cleaned Data
    # -------------------------------
    st.subheader("✨ Cleaned Data")

    st.dataframe(
        data,
        use_container_width=True
    )

    # -------------------------------
    # Download
    # -------------------------------
    csv_data = data.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
