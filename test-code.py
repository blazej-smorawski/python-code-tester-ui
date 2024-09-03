import streamlit as st

from code_editor import code_editor
from utils.frontpage import render_front_page
from utils.runner import display_run_result, run_code
from utils.navbar import display_navbar
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

_RELEASE = True

display_navbar()

_, center, _ = st.columns([1, 5, 1])
with center:
    render_front_page(_RELEASE)
    
    left, right = st.columns([4, 6])

    with left:
        editor_buttons = [{
            "name": "Generuj stronę!",
            "feather": "Play",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0.44rem", "right": "0.4rem"},
            "alwaysOn": True
        }]

        editor_response = code_editor(
            "print('# Hello world!🌎')", key="_frontpage_editor", height=[10, 20], buttons=editor_buttons)
        if editor_response['type'] == "submit":
            result = run_code(editor_response["text"], "")
            st.session_state['result_1']=result

    with right:
        pc = st.get_option('theme.primaryColor')
        bc = st.get_option('theme.backgroundColor')
        sbc = st.get_option('theme.secondaryBackgroundColor')
        tc = st.get_option('theme.textColor')
        if 'result_1' in st.session_state:
            with stylable_container(key="generated_page", css_styles=f"""
                            {{
                                background-color: {sbc};
                                z-index: 999;
                                padding: 10px;
                                border-style: solid;
                                border-width: 1px;
                                border-radius: 5px;
                                border-color: {pc};
                                border-radius: 5px;
                            }}
                            """):
                st.markdown(st.session_state['result_1']['output'])
        else:
            with stylable_container(key="generated_page", css_styles=f"""
                            {{
                                background-color: {sbc};
                                z-index: 999;
                                padding: 10px;
                                border-style: solid;
                                border-width: 1px;
                                border-radius: 5px;
                                border-color: {pc};
                                border-radius: 5px;
                                text-align: center;
                            }}
                            """):
                st.markdown("# ???")

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
