import streamlit as st
from src.blog import display_blog
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

blogs = get_data("blog")

static_pages = [
    st.Page("src/front.py", title="Pomorski Czarodziej", icon="🧙‍♂️"),
    st.Page("src/competition.py", title="Konkurs", icon="📝"),
    st.Page("src/ide.py", title="Programuj!", icon="⌨️"),
    st.Page("src/training.py", title="Zbiór Zadań", icon="📚"),
]

index = 0
dynamic_pages = []
for blog in blogs:
    def blog_page():
            display_blog(f"### {blog['title']}\n\n_{blog['date']}_\n\n{blog['content']}", [{}])

    dynamic_pages.append(
        st.Page(blog_page, icon=blog['icon'], url_path=f'/blog{index}')
    )

static_pages.extend(dynamic_pages)

pg = st.navigation(static_pages, position="hidden")
pg.run()
