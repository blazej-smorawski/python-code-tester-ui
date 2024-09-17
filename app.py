import os
import glob
import streamlit as st
from utils.database import get_data

pc = st.get_option('theme.primaryColor')
bc = st.get_option('theme.backgroundColor')
sbc = st.get_option('theme.secondaryBackgroundColor')
tc = st.get_option('theme.textColor')

st.set_page_config(
            page_title="Pomorski Czarodziej",
            layout="wide",
            page_icon="🧙‍♂️"
        )

static_pages = [
    st.Page("src/front.py", title="Pomorski Czarodziej", icon="🧙‍♂️"),
    st.Page("src/competition.py", title="Konkurs", icon="📝"),
    st.Page("src/ide.py", title="Programuj!", icon="⌨️"),
    st.Page("src/training.py", title="Zbiór Zadań", icon="📚"),
]

index = 0
dynamic_pages = []
directory = 'src/blogs/'
py_files = glob.glob(os.path.join(directory, '*.py'))

for file in py_files:
    dynamic_pages.append(
        st.Page(file, icon='📰')
    )

static_pages.extend(dynamic_pages)

pg = st.navigation(static_pages, position="hidden")
pg.run()
