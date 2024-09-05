
import streamlit as st
from code_editor import code_editor
from utils.navbar import display_navbar
from utils.runner import display_testcase_result, test_code
from utils.database import get_data

display_navbar()

groups = get_data("editions", {"public": {"$eq": True}})
groups_names = [group["name"] for group in groups]
tabs = st.tabs(groups_names)
# Add tab
for element in zip(groups, tabs):
    element[0]["tab"] = element[1]

# Editions
for group in groups:
    with group["tab"]:
        tasks = get_data("tasks", {"edition": {"$eq": group["name"]}})

        col1, col2 = st.columns([1, 2])
        with col1:
            task_name = st.selectbox(
                'Wybierz zadanie', [task["name"] for task in tasks], label_visibility="collapsed")
            task = next(filter(lambda x: x["name"] == task_name, tasks))
            st.markdown(f"### {task_name}")
            st.write(task["description"])

        with col2:
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
                code, key=group["name"]+task["name"]+"_editor", height=[10, 20], buttons=editor_buttons)

            if editor_response['type'] == "submit":
                results = test_code(task, editor_response["text"])
                for result in results:
                    display_testcase_result(result)
