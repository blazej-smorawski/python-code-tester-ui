import streamlit as st

st.set_page_config(
    page_title="Pomorski Czarodziej",
    page_icon="🧙‍♂️"
)

# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header {height: 0rem;}
</style>

"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Title of the app
st.title("🧙 Pomorski Czarodziej")

# Display maintenance message
st.write("Pracujemy nad ulepszeniem naszej strony! Prosimy o cierpliwość i zapraszamy wkrótce! 😊")
