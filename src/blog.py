
import streamlit as st
from utils.navbar import display_navbar
from utils.database import get_data
from streamlit_extras.stylable_container import stylable_container

def display_blog(text, links):
    display_navbar()

    pc = st.get_option('theme.primaryColor')
    bc = st.get_option('theme.backgroundColor')
    sbc = st.get_option('theme.secondaryBackgroundColor')
    tc = st.get_option('theme.textColor')
    _, center, _ = st.columns([1,3,1])
    with center:
        bar, blog = st.columns([3 ,10])
        with bar:
            with stylable_container(key="blog_links", css_styles=f"""
                                {{
                                    background-color: {sbc};
                                    padding: 10px;
                                    border-style: solid;
                                    border-width: 1px;
                                    border-radius: 5px;
                                    border-color: {pc};
                                    border-radius: 5px;
                                    div{{
                                        width:90%;
                                    }}
                                }}
                                """):
                st.write("### 2024")
                st.page_link(
                    "src/ide.py", label="Programuj!", icon="⌨️", use_container_width=False)
                st.page_link(
                    "src/ide.py", label="Programuj!", icon="⌨️", use_container_width=False)
                st.page_link(
                    "src/ide.py", label="Programuj!", icon="⌨️", use_container_width=False)
        with blog:
            with stylable_container(key="blogasddsa", css_styles=f"""
                            {{
                                background-color: {sbc}88;
                                padding: 10px;
                                border-style: solid;
                                border-width: 1px;
                                border-radius: 5px;
                                border-color: {pc};
                                border-radius: 5px;
                                div{{
                                    width:90%;
                                }}
                            }}
                            """):
                st.markdown(text)
