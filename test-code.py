import streamlit as st
import utils.cheatsheet as tips

st.set_page_config(
    page_title="Pomorski Czarodziej",
    layout="wide",
    page_icon="🧙‍♂️"
)

from code_editor import code_editor
from utils.frontpage import render_front_page
from utils.runner import run_code, test_code
from utils.database import get_data

_RELEASE = True

# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header > div:nth-child(1) {height: 0rem;}
</style>

"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

main, training, ide = st.tabs(
    ['🧙‍♂️ O konkursie', '📚 Zbiór Zadań', '⌨️ Programuj!'])

with main:
    _, center, _ = st.columns([1, 5, 1])
    with center:
        render_front_page(_RELEASE)

        st.markdown(
            "Zapraszamy do korzystania z naszego edytora Python w sekcji '⌨️ Programuj!', gdzie możesz dać upust swojej kreatywności kodowania!")

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
            "print('Hello world!🌎')", key="_frontpage_editor", height=[10, 20], buttons=editor_buttons)

        if editor_response['type'] == "submit":
            run_code(editor_response["text"], "")

        st.markdown('''
            ## Regulamin
            Regulamin konkursu na rok 2024 możesz ściągnąć klikając w poniższy przycisk
        ''')

        with open("docs/Pomorski Czarodziej 2024 - Regulamin.pdf", "rb") as file:
            st.download_button(
                label="Regulamin konkursu",
                data=file,
                file_name='Pomorski Czarodziej 2024 - Regulamin.pdf',
                mime='application/pdf')

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
                    test_code(task, editor_response["text"])

with ide:
    _, center, _ = st.columns([1, 6, 1])
    with center:
        st.markdown("## Powodzenia z Pythonem! 🚀")
        st.write("Wejście programu")
        stdin = st.text_area('Wejście programu', label_visibility='collapsed',
                             help="Naciśnij ctrl+enter aby zapisać zmiany")
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
            code, key="_ide_editor", height=[10, 20], buttons=editor_buttons)

        if editor_response['type'] == "submit":
            run_code(editor_response["text"], stdin)

        st.markdown("## Ściąga")
        one, two, three = st.columns([1, 1, 1])
        with one:
            st.markdown(tips.tip_variables())
            st.markdown(tips.tip_maths())

        with two:
            st.markdown(tips.tip_lists())
            st.markdown(tips.tip_loops())

        with three:
            st.markdown(tips.tip_ifs())
            st.markdown(tips.tip_functions())
