from io import BytesIO
import random
import string
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

tasks, tokens = st.tabs(["Zadania", "Tokeny"])

with tasks:

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
    group_name = st.selectbox('Wybierz edycję', [group['name'] for group in groups], key="group_selectbox_2", label_visibility="collapsed")

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
        list = [[x['token'], x['edition']] for x in st.session_state['tokens']]
        df = pd.DataFrame(data = list, columns = ['Token', 'Edycja'])

        df_xlsx = to_excel(df)
        st.download_button(label='📥 Pobierz arkusz z tokenami',
                                    data=df_xlsx ,
                                    file_name= 'tokeny.xlsx')
    