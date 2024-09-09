import streamlit as st
from src.blog import display_blog

pc = st.get_option('theme.primaryColor')
bc = st.get_option('theme.backgroundColor')
sbc = st.get_option('theme.secondaryBackgroundColor')
tc = st.get_option('theme.textColor')

st.set_page_config(
            page_title="Pomorski Czarodziej",
            layout="wide",
            page_icon="🧙‍♂️"
        )

pg = st.navigation([
    st.Page("src/front.py", title="Pomorski Czarodziej", icon="🧙‍♂️"),
    st.Page("src/blog.py", title="Blog", icon="📰"),
    st.Page(lambda: display_blog("# TEST", [{}]), title="Blog", icon="📰", url_path="blog+a"),
    st.Page("src/competition.py", title="Konkurs", icon="📝"),
    st.Page("src/ide.py", title="Programuj!", icon="⌨️"),
    st.Page("src/training.py", title="Zbiór Zadań", icon="📚"),
], position="hidden")
pg.run()
