import streamlit as st

from code_editor import code_editor
from utils.frontpage import render_front_page
from utils.runner import display_run_result, run_code
from utils.navbar import display_navbar

_RELEASE = True

display_navbar()

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
        result = run_code(editor_response["text"], "")
        display_run_result(result)

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
    
