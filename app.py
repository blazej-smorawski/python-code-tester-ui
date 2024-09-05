import streamlit as st

pc = st.get_option('theme.primaryColor')
bc = st.get_option('theme.backgroundColor')
sbc = st.get_option('theme.secondaryBackgroundColor')
tc = st.get_option('theme.textColor')

st.set_page_config(
            page_title="Pomorski Czarodziej",
            layout="wide",
            page_icon="🧙‍♂️"
        )

def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page("src/front.py", title="Pomorski Czarodziej", icon="🧙‍♂️"),
    st.Page("src/blog.py", title="Blog", icon="📰"),
    st.Page("src/competition.py", title="Konkurs", icon="📝"),
    st.Page("src/ide.py", title="Programuj!", icon="⌨️"),
    st.Page("src/training.py", title="Zbiór Zadań", icon="📚"),
    st.Page(page2, title="Second page", icon=":material/favorite:", url_path="test",),
], position="hidden")
pg.run()
