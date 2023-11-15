import streamlit as st

st.set_page_config(
    page_title="test-code",
    layout="wide"
)

import json

import yaml
from utils.runner import test_code
from code_editor import code_editor
from utils.database import get_data, insert_data
import pandas as pd
# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header > div:nth-child(1) {height: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("### Edytor zadań")

if 'task' not in st.session_state:
    st.session_state['task'] = {
        "name": "Czarna magia",
        "edition": "Python 2023",
        "initial-code": "print(1)",
        "description": "Magikuj",
        "test-cases": [
            {
                "input": "1",
                "output": "2",
            }
        ],
    }

task = st.session_state.task

col1, col2 = st.columns([1, 2])
with col1:
    database, form, json_editor, yaml_editor = st.tabs(
        ['Wybierz z bazy', 'Formularz', 'JSON', 'YAML'])
    with database:
        groups = get_data("editions")
        group_name = st.selectbox(
                    'Wybierz edycję', [group['name'] for group in groups], label_visibility="collapsed")

        tasks = get_data("tasks", {"edition": {"$eq": group_name}})
        task_name = st.selectbox(
            'Wybierz zadanie', [task["name"] for task in tasks], label_visibility="collapsed")

        def load():
            task = next(filter(lambda x: x["name"] == task_name, tasks))
            del task["_id"]
            st.session_state.task = task

        st.button("Załaduj z bazy", on_click=load)

    with form:
        st.button("Odśwież", key="refresh_form")

        task["name"] = st.text_input('Nazwa', task["name"])
        task["edition"] = st.text_input('Edycja', task["edition"])
        task["initial-code"] = st.text_area('Kod początkowy', task["initial-code"])
        task["description"] = st.text_area('Opis', task["description"])

        df = pd.DataFrame(task["test-cases"])
        edited_df = st.data_editor(
            df, num_rows="dynamic", use_container_width=True)

        try:
            task["test-cases"] = []
            for index in range(len(edited_df["input"])):
                task["test-cases"].append(
                    {
                        "input": edited_df["input"][index],
                        "output": edited_df["output"][index]
                    }
                )
        except:
            st.warning("Invalid test cases!")

    with json_editor:
        st.button("Odśwież", key="refresh_json")

        code = json.dumps(task, indent=4)
        editor_buttons = [{
            "name": "Zapisz",
            "feather": "Save",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0.44rem", "right": "0.4rem"},
            "alwaysOn": True
        }]
        editor_response = code_editor(
            code, lang="json", key=str(hash(json.dumps(task, sort_keys=True)))+"_json_editor", height=20, buttons=editor_buttons)

        if editor_response['type'] == "submit":
            st.session_state.task = json.loads(editor_response['text'])
            task = st.session_state.task

    with yaml_editor:
        code = yaml.dump(task, indent=4)
        editor_buttons = [{
            "name": "Zapisz",
            "feather": "Save",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0.44rem", "right": "0.4rem"},
            "alwaysOn": True
        }]
        editor_response = code_editor(
            code, lang="yaml", key=str(hash(json.dumps(task, sort_keys=True)))+"_yaml_editor", height=20, buttons=editor_buttons)

        if editor_response['type'] == "submit":
            st.session_state.task = yaml.load(editor_response['text'], Loader=yaml.FullLoader)
            task = st.session_state.task

    if st.button("Wyślij", type="primary"):
        insert_data("tasks", task)


with col2:
    st.markdown(f"### {task['name']}")
    st.markdown(task["description"])
    code = task["initial-code"]
    editor_buttons = [{
        "name": "Uruchom",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
        "alwaysOn": True
    }]

    editor_response = code_editor(
        code, key=str(hash(json.dumps(task, sort_keys=True)))+"_editor", height=[10, 20], buttons=editor_buttons)

    if editor_response['type'] == "submit":
        test_code(task, editor_response["text"])
