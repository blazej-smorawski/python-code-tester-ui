from datetime import datetime
import hmac
from io import BytesIO, StringIO
import random
import string
import pandas as pd
from code_editor import code_editor
import yaml
import json
import streamlit as st

st.set_page_config(
    page_title="test-code",
    layout="wide"
)

from utils.database import get_data, insert_data, replace_data
from utils.runner import display_testcase_result, test_code

# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header {height: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("### Admin UI")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["admin_password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

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

tasks, tokens, submissions = st.tabs(["Zadania", "Tokeny", "Zgłoszenia"])

with tasks:

    col1, col2 = st.columns([1, 2])
    with col1:
        @st.dialog("Wczytaj zadanie")
        def load_task():
            groups = get_data("editions")
            group_name = st.selectbox(
                'Wybierz edycję', [group['name'] for group in groups], label_visibility="collapsed")

            tasks = get_data("tasks", {"edition": {"$eq": group_name}})
            task_name = st.selectbox(
                'Wybierz zadanie', [task["name"] for task in tasks], label_visibility="collapsed")

            def load():
                task = next(filter(lambda x: x["name"] == task_name, tasks))
                st.session_state.task = task

            if st.button("Załaduj z bazy", on_click=load):
                st.rerun()

            uploaded_yaml = st.file_uploader("Wczytaj plik `.yaml`")
            if uploaded_yaml is not None:
                stringio = StringIO(uploaded_yaml.getvalue().decode("utf-8"))
                string_data = stringio.read()

                task = yaml.load(string_data, Loader=yaml.FullLoader)
                st.session_state.task = task
                st.rerun()

            uploaded_json = st.file_uploader("Wczytaj plik `.json`")
            if uploaded_json is not None:
                stringio = StringIO(uploaded_json.getvalue().decode("utf-8"))
                string_data = stringio.read()

                task = json.loads(string_data)
                st.session_state.task = task
                st.rerun()

        if st.button("Wczytaj zadanie"):
            load_task()

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
                'input': st.column_config.TextColumn('Input'),
                'output': st.column_config.TextColumn('Output'),
                'public': st.column_config.CheckboxColumn('Public')
            }
            st.session_state["new_test_cases"] = st.data_editor(
                task["test-cases"], key="test_cases_editor", column_config=config, num_rows="dynamic", use_container_width=True)

            def validate_test_cases(df):
                for entry in df:
                    # Validate and cast 'input' to string
                    if not isinstance(entry['input'], str):
                        entry['input'] = str(entry['input']) if entry['input'] is not None else ""

                    # Validate and cast 'output' to string
                    if not isinstance(entry['output'], str):
                        entry['output'] = str(entry['output']) if entry['output'] is not None else ""

                    # Validate and cast 'public' to boolean
                    if 'public' not in entry or entry['public'] is None:
                        entry['public'] = False
                    else:
                        entry['public'] = bool(entry['public'])

            def save_test_cases():
                validate_test_cases(st.session_state["new_test_cases"])
                task["test-cases"] = st.session_state["new_test_cases"]

            st.button("Zapisz zmiany w przypadkach testowych",
                      on_click=save_test_cases)

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

        task_without_id = json.dumps(
            {i: task[i] for i in task if i != "_id"}, sort_keys=True)
        editor_response = code_editor(
            code, key=str(hash(task_without_id))+"_editor", height=[10, 20], buttons=editor_buttons)

        if editor_response['type'] == "submit":
            results = test_code(task, editor_response["text"])
            for result in results:
                display_testcase_result(result)

with tokens:
    def generate_new_tokens(num_tokens, existing_tokens):
        new_tokens = set()  # Using a set to store unique tokens

        while len(new_tokens) < num_tokens:
            ntries = 0
            max_tries = 3
            while ntries < max_tries:
                # Generate two random letters
                letters = ''.join(random.choices(string.ascii_uppercase, k=2))
                # Generate four random digits
                numbers = ''.join(random.choices(string.digits, k=4))
                # Combine letters and numbers to form a token
                token = letters + numbers

                if token not in existing_tokens and token not in new_tokens:
                    new_tokens.add(token)
                    break
                else:
                    st.error("Kolizja tokenów!")
                    ntries += 1

            if ntries == max_tries:
                new_tokens = set()
                break

        return list(new_tokens)

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.close()
        processed_data = output.getvalue()
        return processed_data

    groups = get_data("editions")
    group_name = st.selectbox('Wybierz edycję', [
                              group['name'] for group in groups], key="group_selectbox_2", label_visibility="collapsed")

    tokens_count = 0
    tokens_count_string = st.text_input('Liczba tokenów', "0")
    try:
        tokens_count = int(tokens_count_string)
    except:
        st.error("Niepoprawna liczba tokenów!")

    import pandas as pd

    if st.button("Generuj tokeny"):
        existing_entries = get_data("tokens")
        existing_tokens = [x['token'] for x in existing_entries]
        new_tokens = generate_new_tokens(tokens_count, existing_tokens)

        if len(new_tokens) != 0:
            new_entries = []
            for token in new_tokens:
                entry = {'token': token, 'edition': group_name}
                new_entries.append(entry)
                insert_data("tokens", entry)
            st.session_state['tokens'] = new_entries
            st.success("Generowanie tokenów ukończone")
        else:
            if 'tokens' in st.session_state:
                del st.session_state['tokens']
            st.error("Generowanie tokenów nie udało się")

    if 'tokens' in st.session_state:
        tokens_list = [[x['token'], x['edition']] for x in st.session_state['tokens']]
        df = pd.DataFrame(data=tokens_list, columns=['Token', 'Edycja'])

        df_xlsx = to_excel(df)
        st.download_button(label='📥 Pobierz arkusz z tokenami',
                           data=df_xlsx,
                           file_name='tokeny.xlsx')

with submissions:
    submissions = get_data("submissions")

    # Date input
    selected_date = st.date_input("Wybierz datę", datetime.today())

    # Filter entries by selected date
    filtered_entries = [
        entry for entry in submissions if entry["timestamp"].date() == selected_date]

    # Group entries by ID
    grouped_entries = {}
    for entry in filtered_entries:
        entry_id = entry["id"]
        if entry_id not in grouped_entries:
            grouped_entries[entry_id] = []
        grouped_entries[entry_id].append(entry)

    # Sort entries within each group by timestamp
    for entry_id, entries_list in grouped_entries.items():
        entries_list.sort(key=lambda x: x["timestamp"])

    # Create a selectbox to choose an entry ID
    selected_entry_id = st.selectbox(
        "Wybierz ID", list(grouped_entries.keys()))

    # Display the selectbox for dates for the selected entry
    if selected_entry_id in grouped_entries:
        # Choosing the latest entry for inspection
        selected_entry = grouped_entries[selected_entry_id][-1]
        sorted_dates = sorted([entry["timestamp"]
                              for entry in grouped_entries[selected_entry_id]])
        selected_date_index = st.selectbox("Wybierz wersję zgłoszenia", range(len(
            sorted_dates)), format_func=lambda x: sorted_dates[x].strftime('%Y-%m-%d %H:%M:%S'))
        selected_entry = grouped_entries[selected_entry_id][selected_date_index]

        for key, value in selected_entry["exam_results"].items():
            result = value["result"]
            st.markdown(f"### {key} [{result*100:.2f}/100.00]")
            st.code(value["code"], language="python")
    else:
        st.write("Brak zadania.")
