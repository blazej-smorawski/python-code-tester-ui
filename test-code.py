import psycopg2
import re
import requests
import streamlit as st
import streamlit as st
from code_editor import code_editor

st.set_page_config(
    page_title="test-code",
    layout="wide"
)

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query, *args):
    with conn.cursor() as cur:
        cur.execute(query, args)
        return cur.fetchall()

# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header > div:nth-child(1) {height: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

main, training, current = st.tabs(
    ['🧙‍♂️ O konkursie', '📚 Zbiór Zadań', '🐍 Python 2024'])

with main:
    st.markdown("# Pomorski Czarodziej")
    st.markdown("")
    st.markdown('''
        ## Cel konkursu
        Celem jaki przyświeca nam przy organizacji tego konkursu jest rozwijanie zainteresowań algorytmiką i technologią informatyczną. Zależ nam na popularyzowaniu programowania w klasach szkół podstawowych.
        Odpowiadamy na propozycję zmian w podstawie programowej wprowadzającą elementy programowania od najmłodszych lat.
        Konkurs ma sprzyjać rozwojowi uzdolnień i zainteresowań, pobudzać do twórczego myślenia, wspomagać zdolności stosowania zdobytej wiedzy w praktyce oraz docelowo przyczynić się do lepszego przygotowania uczniów do nauki w szkołach wyższego stopnia.
        Chcemy pokazać, że używając powszechnie bardzo popularnego języka programowania jakim jest Python, można zaszczepiać koncepty programistyczne już w szkole podstawowej.
        Konkurs jest darmowy. Udział mogą wziąć wszystkie szkoły prywatne i publiczne z województwa pomorskiego.
    ''')

with training:
    groups = run_query('SELECT * FROM "group"')
    groups_names = [group[1] for group in groups]
    tabs = st.tabs(groups_names)
    # Add tab and key to each group
    groups = [(*element[0], element[1])
              for element in zip(groups, tabs)]

    # Editions
    for group in groups:
        with group[2]:
            tasks = run_query(
                'SELECT * FROM "tasks" WHERE "group_id" = %s', (group[0]))

            col1, col2 = st.columns([1, 2])
            with col1:
                task_name = st.selectbox(
                    'Wybierz zadanie', [task[1] for task in tasks], label_visibility="hidden")

                task = next(filter(lambda x: x[1] == task_name, tasks))
                st.markdown(f"### {task_name}")
                st.write(task[3])

            with col2:
                code = "print(1)"
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
                    code, key=group[1]+"_editor", height=[10, 20], buttons=editor_buttons)

                if editor_response['type'] == "submit":
                    testcases = run_query(
                        'SELECT * FROM "testcase" WHERE "taskId" = %s', (task[0]))
                    
                    for testcase in testcases:
                        url = 'https://piston-dev.kubernetes.blazej-smorawski.com/api/v2/execute'
                        payload = {
                            "language": "python",
                            "version": "3.10.0",
                            "files": [
                                {
                                    "name": "code.py",
                                    "content": editor_response['text']
                                }
                            ],
                            "stdin": testcase[2].replace('\\n', '\n') # Replace \\n with \n
                        }
                        req = requests.post(url, json=payload)
                        #st.write(req.status_code)
                        #st.write(req.json())
                        result = req.json()
                        
                        if req.status_code == 200 and result['run']['code'] == 0 and re.match(testcase[3].replace('\\n', '\n'), result['run']['stdout']):
                            st.success(f"Test zaliczony", icon="✅")
                        else:
                            st.error(f"Test niezaliczony", icon="❌")

                        input_col, output_col= st.columns([3,3])
                        input_col.write("Wejście programu")
                        input_col.code(testcase[2].replace('\\n', '\n'))
                        output_col.write("Wyjście programu")
                        output_col.code(result['run']['stdout'])

                        if result['run']['stderr'] != "":
                            st.write("Błędy wykonania programu:")
                            st.code(result['run']['stderr'])
