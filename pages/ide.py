import streamlit as st
import utils.cheatsheet as tips
from code_editor import code_editor
from utils.navbar import display_navbar
from utils.runner import display_run_result, run_code

display_navbar()

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
    
    code = ""
    editor_response = code_editor(
        code, key="_ide_editor", height=[10, 20], buttons=editor_buttons)

    if editor_response['type'] == "submit":
        result = run_code(editor_response["text"], stdin)
        display_run_result(result)

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