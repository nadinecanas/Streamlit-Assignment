import streamlit as st
import pandas as pd

st.title("📊 DataFrame Viewer")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if df.shape[1] < 5:
        st.error("The uploaded file must have at least 5 columns.")
    else:
        st.header("Dataset Preview")

        if st.checkbox("Show raw data"):
            st.dataframe(df)

        column = st.selectbox("Select a column to filter by", df.columns)

        unique_values = df[column].unique()
        selected_value = st.selectbox(f"Filter {column} by:", unique_values)

        filtered_df = df[df[column] == selected_value]
        st.subheader(f"Filtered Data (where {column} = {selected_value})")
        st.dataframe(filtered_df)
else:
    st.info("Please upload a CSV file to get started.")
