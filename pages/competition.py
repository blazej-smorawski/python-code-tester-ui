import copy
import datetime
import json
import time
import streamlit as st
from code_editor import code_editor
from utils.database import get_data, insert_data
from utils.navbar import display_navbar
from utils.runner import display_testcase_result, test_code
from utils.telemetry import log_telemetry

display_navbar()

if 'submission' not in st.session_state:
    st.session_state['submission'] = {}

current_submission = st.session_state['submission']

_, center, _ = st.columns([1, 4, 1])
with center:
    tutorial = st.expander("Instrukcja", expanded=True)

with tutorial:
    def image_html(path):
        return f'<img src="{path}" style="max-width: 100%;">'
    st.markdown(f"""
                1. Zaczynamy! Wpisz swój kod uczestnika poniżej.
                2. Teraz czas na rozwiązanie zadań. Możesz je wybierać w dowolnej kolejności. 
                Pamiętaj o regularnym zapisywaniu swoich postępów za pomocą przycisku `Zapisz rozwiązanie` 
                przy każdym zadaniu. Dzięki temu będziesz mógł/a uniknąć zgubienia swojej pracy! 📝 {image_html("/app/static/save.jpeg")}
                3. Gdy już skończysz, kliknij przycisk `Zgłoś rozwiązanie`, aby przesłać swoje zadania. 
                Nie martw się, możesz wysłać swoje rozwiązania wielokrotnie! 📤 {image_html("/app/static/submit.jpeg")}
                4. Upewnij się, że przesłane rozwiązanie zawiera wszystkie ostateczne poprawki. 
                Sprawdź to! 🔍 {image_html("/app/static/check.jpeg")}
                """, unsafe_allow_html=True)

st.markdown("## Podaj kod uczestnika")

users_token = st.text_input('Podaj kod uczestnika',
                            "", label_visibility="hidden")
found_token_data = get_data("tokens", {"token": {"$eq": users_token}})

if len(found_token_data) == 0:
    st.error("Niepoprawny token")
    st.stop()

found_token = found_token_data[0]
found_edition_data = get_data("editions", {"public": {"$eq": False}, "active": {
                              "$eq": True}, "name": {"$eq": found_token['edition']}})

if len(found_edition_data) == 0:
    st.error("Nieważny token!")
    st.stop()

# Both token and edition are correct
token = found_token['token']
group = found_edition_data[0]

if 'exam_start_recorded' not in st.session_state:
    log_telemetry({'event': "exam started"}, token)
    st.session_state['exam_start_recorded'] = True

group_name = group['name']
start_date = group["start"]
end_date = group["end"]

# Get the current datetime
current_time = datetime.datetime.now().replace(microsecond=0)

# Check if it's before the start
if current_time < start_date:
    st.session_state['active'] = False
    time_remaining = start_date - current_time
    # Custom format
    formatted_time_remaining = "{} dni {:02} godzin {:02} minut {:02} sekund".format(
        time_remaining.days,
        time_remaining.seconds // 3600,  # hours
        (time_remaining.seconds // 60) % 60,  # minutes
        time_remaining.seconds % 60  # seconds
    )
    st.markdown(
        f'<div style="text-align: center;"><h3>Konkurs rozpocznie się za</h3></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align: center;"><h2>{formatted_time_remaining}</h2></div>', unsafe_allow_html=True)
    time.sleep(1)
    st.rerun()
# Check if it's after the end
elif current_time > end_date:
    st.markdown(
        f'<div style="text-align: center;"><h3>Edycja {group_name} dobiegła końca!</h3></div>', unsafe_allow_html=True)
    st.stop()
# If none of above clauses is true it means we can display competition

tasks = get_data("tasks", {"edition": {"$eq": group["name"]}})

number = 1
for task in tasks:
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

        submission_state_container = st.container()

        if editor_response['type'] == "submit":
            log_telemetry({'event': "code tested", 'task': task_name,
                          'code': editor_response["text"]}, token)
            current_submission[task_name] = editor_response["text"]

            results = test_code(task, editor_response["text"])
            for result in results:
                display_testcase_result(result)

        if task_name in current_submission:
            submission_state_container.success(
                f"Rozwiązanie zapisane. Użyj przycisku *Zgłoś rozwiązanie* na dole strony, aby zakończyć podejście", icon="✅")
    st.divider()

_, center, _ = st.columns([1, 1, 1])
with center:
    if st.button("Zgłoś rozwiązanie", use_container_width=True, type="primary"):
        with st.status("Wysyłam rozwiązanie..."):
            st.write("Sprawdzam zadania...")
            exam = {"name": group_name, "tasks": {}}
            exam_results = {}
            for task in tasks:
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
                exam["tasks"][task_name] = task["description"]

            st.write("Zapisuję wersję konkursu...")
            # Might not be stable
            hash = hash(json.dumps(exam, sort_keys=True))

            st.write("Zapisuję dane w bazie...")
            exam_in_db = get_data("exams", {"hash": {"$eq": hash}})
            if not exam_in_db:
                insert_data("exams", {"hash": hash, "exam": exam})

            insert_data("submissions", {
                        "id": token, "exam_hash": hash, "timestamp": datetime.datetime.now(), "exam_results": exam_results})
            st.session_state['sent_submission'] = copy.deepcopy(current_submission)
            st.session_state['solution_id'] = token
            st.write("Sukces!")
        st.success(
            "Twoje rozwiązanie zostało przyjęte, dziękujemy za udział w konkursie!", icon="✅")

    if 'solution_id' in st.session_state:
        solution_id = st.session_state['solution_id']
        st.markdown(
            f'<div style="text-align: center;"><h4>Twój kod:</h1></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align: center;"><h1>{solution_id}</h1></div>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("### Sprawdź poprawność wysłanego rozwiązania!")
            for name, code in st.session_state['sent_submission'].items():
                st.markdown(f"#### {name}")
                st.code(code, language="python")
