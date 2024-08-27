
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

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
    container = st.container(border=False)

    pc = st.get_option('theme.primaryColor')
    bc = st.get_option('theme.backgroundColor')
    sbc = st.get_option('theme.secondaryBackgroundColor')
    tc = st.get_option('theme.textColor')
    with stylable_container(key="heading", css_styles=f"""
                            {{
                                background-color: {sbc};
                                //position: fixed; fixed looks fire but lags abit
                                z-index: 999;
                                padding: 10px;
                                border-style: solid;
                                border-width: 1px;
                                border-radius: 5px;
                                border-color: {pc};
                                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                            }}
                            """):

        left, center, right =  st.columns([1,4,3])
        with left:
            center = grid(1, vertical_align="center")
            center.page_link(
                "test-code.py", label="Pomorski Czarodziej", icon="🧙‍♂️", use_container_width=False)
        with right:
            navigation_bar = grid(3, vertical_align="center")
            navigation_bar.page_link(
                "pages/training.py", label="Zbiór Zadań", icon="📚", use_container_width=True)
            navigation_bar.page_link(
                "pages/ide.py", label="Programuj!", icon="⌨️", use_container_width=True)
            navigation_bar.page_link(
                "pages/competition.py", label="Konkurs", icon="📝", use_container_width=True)
    #st.container(height=60, border=False)
