import streamlit as st

st.set_page_config(
    page_title="test-code",
    layout="wide"
)

import pandas as pd
from utils.database import get_data, insert_data

from code_editor import code_editor
from utils.runner import run_code


# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header > div:nth-child(1) {height: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("# Edytor zadań")

col1, col2 = st.columns([1, 2])
with col1:
    task = {}
    task["name"] = st.text_input('Nazwa', 'Czarna magia')
    task["edition"] = st.text_input('Edycja', 'Python 2023')
    task["initial-code"] = st.text_area('Kod początkowy', 'print(1)')
    task["description"] = st.text_area('Opis', 'Magikuj')
    st.markdown(task["description"])

    df = pd.DataFrame(
        [
            {"input": "2\\n2", "output": "4", },
        ]
    )
    edited_df = st.data_editor(
        df, num_rows="dynamic", use_container_width=True)

    # try:
    task["test-cases"] = []
    for index in range(len(edited_df["input"])):
        task["test-cases"].append(
            {
                "input": edited_df["input"][index],
                "output": edited_df["output"][index]
            }
        )
    # except:
    #     st.error("Niepoprawny format przypadków testowych")
    if st.button("Wyślij", type="primary"):
        insert_data("tasks", task)


with col2:
    code = task["initial-code"]
    editor_buttons = [{
        "name": "Uruchom",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"}
    }]
    editor_response = code_editor(
        code, key=task["name"]+str(task["test-cases"])+task["initial-code"]+"_editor", height=[10, 20], buttons=editor_buttons)

    if editor_response['type'] == "submit":
        run_code(task, editor_response["text"])
