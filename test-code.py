import streamlit as st

st.set_page_config(
    page_title="test-code",
    layout="wide"
)

from code_editor import code_editor
from utils.runner import run_code
from utils.database import get_data

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
                    run_code(task, editor_response["text"])
