
import streamlit as st
from streamlit_extras.grid import grid


def display_navbar():
    if not 'config_done' in st.session_state:
        st.set_page_config(
            page_title="Pomorski Czarodziej",
            layout="wide",
            page_icon="🧙‍♂️"
        )
        st.session_state['config_done'] = True

    # Improve page layout
    hide_streamlit_style = """
    <style>
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
        #root > div:nth-child(1) > div > div > div > header {height: 0rem;}
    </style>

    """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 4, 1])
    container = center.container(border=True)
    with container:
        navigation_bar = grid(4)
        navigation_bar.page_link(
            "test-code.py", label="O nas", icon="🧙‍♂️", use_container_width=True)
        navigation_bar.page_link(
            "pages/training.py", label="Zbiór Zadań", icon="📚", use_container_width=True)
        navigation_bar.page_link(
            "pages/ide.py", label="Programuj!", icon="⌨️", use_container_width=True)
        navigation_bar.page_link(
            "pages/competition.py", label="Konkurs", icon="📝", use_container_width=True)
