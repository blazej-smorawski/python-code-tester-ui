import os
import glob
import re
from datetime import datetime
import streamlit as st
from utils.navbar import display_navbar
from utils.database import get_data
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

NAME_TO_DISPLAY = {
    "src/blogs/blog_26_02_2026.py": {"title": "Pomorski Czarodziej 2026", "icon": "🎉"},
    "src/blogs/blog_17_10_2024.py": {
        "title": "Cześć młodzi programiści!",
        "icon": "👋",
    },
    "src/blogs/blog_07_10_2024.py": {"title": "Zapraszamy na nasz kanał", "icon": "▶️"},
}


def extract_date_from_filename(file_path):
    filename = os.path.basename(file_path)
    match = re.search(r"(\d{2}_\d{2}_\d{4})", filename)
    if match:
        return datetime.strptime(match.group(1), "%d_%m_%Y")
    return datetime.min


def display_blog(text, links):
    display_navbar()

    pc = st.get_option("theme.primaryColor")
    bc = st.get_option("theme.backgroundColor")
    sbc = st.get_option("theme.secondaryBackgroundColor")
    tc = st.get_option("theme.textColor")
    _, center, _ = st.columns([1, 4, 1])
    with center:
        # bar, blog = st.columns([3 ,10])
        # with bar:
        with st.container(horizontal=True, border=False):
            # st.write("### 2024")
            directory = "src/blogs/"
            py_files = sorted(
                glob.glob(os.path.join(directory, "*.py")),
                key=extract_date_from_filename,
                reverse=True,
            )
            #links_grid = grid(3, vertical_align="center")
            for file in py_files:
                props = NAME_TO_DISPLAY[file]
                st.page_link(
                    file,
                    label=f"{props['title']}",
                    icon=f"{props['icon']}",
                    use_container_width=False,
                )
        # with blog:
        with stylable_container(
            key="blogasddsa",
            css_styles=f"""
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
                        """,
        ):
            st.markdown(text, unsafe_allow_html=True)
