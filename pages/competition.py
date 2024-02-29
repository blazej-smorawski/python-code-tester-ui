import json
import random
import streamlit as st
from code_editor import code_editor
from utils.database import get_data, insert_data
from utils.navbar import display_navbar
from utils.runner import display_testcase_result, test_code

display_navbar()

if 'submission' not in st.session_state:
    st.session_state['submission'] = {}

current_submission = st.session_state['submission']

groups = get_data("editions", {"name": {"$eq": "Python 2024"}})
group = groups[0]

tasks = get_data("tasks", {"edition": {"$eq": group["name"]}})
seen_names = set()
filtered_tasks = []
for task in tasks:
    if task["name"] not in seen_names:
        filtered_tasks.append(task)
        seen_names.add(task["name"])

number = 1
for task in filtered_tasks:
    task_name = task["name"]
    st.markdown(f"### {number}. {task_name}")
    number += 1

    col1, col2 = st.columns([1, 2])
    with col1:
        task_description = st.container()
        task_description.write(task["description"])

    with col2:
        code = task["initial-code"]
        editor_buttons = [{
            "name": "Zapisz rozwiązanie",
            "feather": "Save",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0.44rem", "right": "0.4rem"},
            "alwaysOn": True
        }]
        editor_response = code_editor(
            code, key=group["name"]+task["name"]+"_editor", height="500px", buttons=editor_buttons)

        if editor_response['type'] == "submit":
            current_submission[task_name] = editor_response["text"]

            results = test_code(task, editor_response["text"])
            for result in results:
                display_testcase_result(result)
    st.divider()

_, center, _ = st.columns([1, 1, 1])
with center:
    if st.button("Zgłoś rozwiązanie", use_container_width=True):
        with st.status("Wysyłam rozwiązanie..."):
            st.write("Sprawdzam zadania...")
            exam = {}
            exam_results = {}
            for task in filtered_tasks:
                task_name = task["name"]
                code = ""
                if task_name in current_submission:
                    code = current_submission[task_name]

                results = test_code(task, code, private=True)
                passed_count = sum(
                    1 for res in results if res.get("passed", True))
                tests_count = len(task["test-cases"])

                exam_results[task_name] = {
                    "result": passed_count/tests_count, "code": code}
                exam[task_name] = task["description"]

            st.write("Zapisuję wersję konkursu...")
            # Might not be stable
            hash = hash(json.dumps(exam, sort_keys=True))

            st.write("Zapisuję dane w bazie...")
            exam_in_db = get_data("exams", {"hash": {"$eq": hash}})
            if not exam_in_db:
                insert_data("exams", {"hash": hash, "exam": exam})

            solution_id = random.randint(0, 1e10)
            insert_data("submissions", {"id": solution_id, "exam_hash": hash, "exam_results": exam_results})
            st.session_state['solution_id'] = solution_id
            st.write("Sukces!")

    if 'solution_id' in st.session_state:
        st.success(
            "Twoje rozwiązanie zostało przyjęte, dziękujemy za udział w konkursie!", icon="✅")
        solution_id = st.session_state['solution_id']
        st.markdown(f'<div style="text-align: center;"><h4>Twój kod:</h1></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center;"><h1>{solution_id}</h1></div>', unsafe_allow_html=True)