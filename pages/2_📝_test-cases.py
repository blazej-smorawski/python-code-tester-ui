import streamlit as st
import pandas as pd

df = pd.DataFrame(columns=["Input", "OutputRegex"])
edited_df = st.experimental_data_editor(df, num_rows="dynamic")
json = edited_df.to_json(orient="records")
st.download_button(
    label="Download test cases as JSON",
    data=json,
    file_name='test_cases.txt',
    mime='text/plain',
)