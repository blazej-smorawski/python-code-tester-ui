import pandas as pd
from utils.database import get_data, insert_data, replace_data
from code_editor import code_editor
from utils.runner import display_testcase_result, test_code
import yaml
import json
import streamlit as st

st.set_page_config(
    page_title="test-code",
    layout="wide"
)


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
        "edition": "SANDBOX",
        "initial-code": "print(1)",
        "description": "Magikuj",
        "test-cases": [
            {
                "input": "1",
                "output": "2",
                "public": False
            }
        ],
    }

task = st.session_state.task

col1, col2 = st.columns([1, 2])
with col1:
    groups = get_data("editions")
    group_name = st.selectbox(
        'Wybierz edycję', [group['name'] for group in groups], label_visibility="collapsed")

    tasks = get_data("tasks", {"edition": {"$eq": group_name}})
    task_name = st.selectbox(
        'Wybierz zadanie', [task["name"] for task in tasks], label_visibility="collapsed")

    def load():
        task = next(filter(lambda x: x["name"] == task_name, tasks))
        st.session_state.task = task

    st.button("Załaduj z bazy", on_click=load)

    form = st.form(key="task_editor_form")

    with form:
        task["name"] = st.text_input('Nazwa', task["name"])
        task["edition"] = st.text_input('Edycja', task["edition"])
        task["initial-code"] = st.text_area('Kod początkowy',
                                            task["initial-code"])
        task["description"] = st.text_area('Opis', task["description"])

        st.form_submit_button('Zapisz zmiany')

    test_cases = st.container(border=True)
    with test_cases:
        config = {
            'input' : st.column_config.TextColumn('Input'),
            'output' : st.column_config.TextColumn('Output'),
            'public' : st.column_config.CheckboxColumn('Public')
        }
        st.session_state["new_test_cases"] = st.data_editor(
            task["test-cases"], key="test_cases_editor", column_config=config, num_rows="dynamic", use_container_width=True)

        def save_test_cases():
            task["test-cases"] = st.session_state["new_test_cases"]

        st.button("Zapisz zmiany w przypadkach testowych", on_click=save_test_cases)

    if st.button("Usuń *_id*", type="secondary", use_container_width=True):
        if "_id" in task:
            del task["_id"]

    check = st.container(border=True)
    with check:
        st.markdown("#### Sprawdź zawartość zadania ")
        st.write(task)

    if st.button("Wyślij", type="primary", use_container_width=True):
        try:
            insert_data("tasks", task, keep_id=True)
        except Exception as e:
            st.error(f"Błąd wysyłania zadania: {str(e)}")
        finally:
                st.success("Wysyłanie zakończone sukcesem")

    if st.button("Aktualizuj", type="primary", use_container_width=True):
        if "_id" not in task:
            st.error("Brak wartości **_id**")
        else:
            try:
                replace_data("tasks", task)
            except:
                st.error("Błąd aktualizacji zadania")
            finally:
                st.success("Aktualizacja zakończona sukcesem")


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

    task_without_id = json.dumps({i:task[i] for i in task if i!="_id"}, sort_keys=True)
    editor_response = code_editor(
        code, key=str(hash(task_without_id))+"_editor", height=[10, 20], buttons=editor_buttons)

    if editor_response['type'] == "submit":
        results = test_code(task, editor_response["text"])
        for result in results:
            display_testcase_result(result)
