
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

def display_navbar():
    if not 'config_done' in st.session_state:
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

        left, center, right =  st.columns([4,1,6])
        with left:
            center = grid(2, vertical_align="center")
            center.page_link(
                "src/front.py", label="Pomorski Czarodziej", icon="🧙‍♂️", use_container_width=True)
            gh_logo = f"""
            <svg height=40>
                <path stroke={pc} fill={pc} d="M12 1C5.9225 1 1 5.9225 1 12C1 16.8675 4.14875 20.9787 8.52125 22.4362C9.07125 22.5325 9.2775 22.2025 9.2775 21.9137C9.2775 21.6525 9.26375 20.7862 9.26375 19.865C6.5 20.3737 5.785 19.1912 5.565 18.5725C5.44125 18.2562 4.905 17.28 4.4375 17.0187C4.0525 16.8125 3.5025 16.3037 4.42375 16.29C5.29 16.2762 5.90875 17.0875 6.115 17.4175C7.105 19.0812 8.68625 18.6137 9.31875 18.325C9.415 17.61 9.70375 17.1287 10.02 16.8537C7.5725 16.5787 5.015 15.63 5.015 11.4225C5.015 10.2262 5.44125 9.23625 6.1425 8.46625C6.0325 8.19125 5.6475 7.06375 6.2525 5.55125C6.2525 5.55125 7.17375 5.2625 9.2775 6.67875C10.1575 6.43125 11.0925 6.3075 12.0275 6.3075C12.9625 6.3075 13.8975 6.43125 14.7775 6.67875C16.8813 5.24875 17.8025 5.55125 17.8025 5.55125C18.4075 7.06375 18.0225 8.19125 17.9125 8.46625C18.6138 9.23625 19.04 10.2125 19.04 11.4225C19.04 15.6437 16.4688 16.5787 14.0213 16.8537C14.42 17.1975 14.7638 17.8575 14.7638 18.8887C14.7638 20.36 14.75 21.5425 14.75 21.9137C14.75 22.2025 14.9563 22.5462 15.5063 22.4362C19.8513 20.9787 23 16.8537 23 12C23 5.9225 18.0775 1 12 1Z"></path>
            </svg>"""
            center.markdown(f"<a href=\"https://github.com/blazej-smorawski/python-code-tester-ui\">{gh_logo}</a>", unsafe_allow_html=True)
        with right:
            navigation_bar = grid(4, vertical_align="center")
            navigation_bar.page_link(
                "src/blogs/blog_17_10_2024.py", label="Aktualności", icon="📰", use_container_width=True)
            navigation_bar.page_link(
                "src/training.py", label="Zbiór Zadań", icon="📚", use_container_width=True)
            navigation_bar.page_link(
                "src/ide.py", label="Programuj!", icon="⌨️", use_container_width=True)
            navigation_bar.page_link(
                "src/competition.py", label="Konkurs", icon="📝", use_container_width=True)
    #st.container(height=60, border=False)
