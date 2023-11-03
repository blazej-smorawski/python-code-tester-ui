import streamlit as st

st.set_page_config(
    page_title="test-code",
    layout="centered"
)

from code_editor import code_editor
from utils.runner import run_code
from utils.database import get_data
from PIL import Image

# Improve page layout
hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
    #root > div:nth-child(1) > div > div > div > header > div:nth-child(1) {height: 0rem;}
</style>

"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

main, training, current = st.tabs(
    ['🧙‍♂️ O konkursie', '📚 Zbiór Zadań', '🐍 Python 2024'])

with main:
    st.markdown("# Pomorski Czarodziej")
    st.markdown("")
    st.markdown('''
        ## Cel konkursu
        Celem jaki przyświeca nam przy organizacji tego konkursu jest rozwijanie zainteresowań algorytmiką i technologią informatyczną. Zależ nam na popularyzowaniu programowania w klasach szkół podstawowych.
        Odpowiadamy na propozycję zmian w podstawie programowej wprowadzającą elementy programowania od najmłodszych lat.
        Konkurs ma sprzyjać rozwojowi uzdolnień i zainteresowań, pobudzać do twórczego myślenia, wspomagać zdolności stosowania zdobytej wiedzy w praktyce oraz docelowo przyczynić się do lepszego przygotowania uczniów do nauki w szkołach wyższego stopnia.
        Chcemy pokazać, że używając powszechnie bardzo popularnego języka programowania jakim jest Python, można zaszczepiać koncepty programistyczne już w szkole podstawowej.
        Konkurs jest darmowy. Udział mogą wziąć wszystkie szkoły prywatne i publiczne z województwa pomorskiego.
    ''')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
            ## Historia konkursu
            Konkurs programowania dla szkół podstawowych organizujemy wspólnie z nauczycielami od 2010 roku. W pierwszej, kameralnej edycji uczestniczyły jedynie 4 szkoły. 
            Na przestrzeni lat konkurs zyskiwał coraz większą popularności i bywało, że udział brała nawet ponad setka dzieci z prawie dwudziestu pomorskich szkół. 
            Podczas poprzednich edycji aktywnie współpracowaliśmy z Kuratorium Oświaty w Gdańsku. Od 2022 zmieniamy formułę konkursu, wychodząc naprzeciw nowym trendom na rynku i zmianą programowym. 
            Stosowany do tej pory Baltiee zastępujemy językiem Python.
            
            Już tradycją stało się, że gala finałowa konkursu oraz wręczenie nagród odbywa się w siedzibie firmy Intel Technology Poland, gdzie pokazujemy, jak wygląda praca programisty komputerowego, 
            oprowadzamy uczestników po biurze oraz przeprowadzamy krótkie lekcje związane z technologią informacyjną.
        ''')

    with col2:
        image01 = Image.open('img/pic01.jpg')
        st.image(image01)

        image02 = Image.open('img/pic02.jpg')
        st.image(image02)

        image03 = Image.open('img/pic03.jpg')
        st.image(image03)

    with col3:
        image04 = Image.open('img/pic04.jpg')
        st.image(image04)

        image05 = Image.open('img/pic05.jpg')
        st.image(image05)

        image06 = Image.open('img/pic06.jpg')
        st.image(image06)


    st.markdown('''
        ## Kim jesteśmy?
        Jesteśmy grupą wolontariuszy pracujących nad rozwojem oprogramowania w firmie Intel Technology Poland. 
        Nasza praca daje nam na co dzień niesamowitą satysfakcję i wierzymy, że można cieszyć się algorytmiką, analizą i rozwiązywaniem problemów oraz programowaniem niezależnie od wieku.
        Chcemy pokazać nasz świat najmłodszym, aby nawet ci, którzy nigdy nie pomyśleliby, żeby zainteresować się informatyką (albo uważają, że taka praca jest trudna, nudna i żmudna), zobaczyli, 
        jak wygląda praca informatyka programisty i co faktycznie kryje się za tym monitorem pełnym niezrozumiałych znaków.                
    ''')

    image07 = Image.open('img/pic07.jpg')
    st.image(image07)
                
    st.markdown('''
        ## Regulamin
        Regulamin konkursu na rok 2024 możesz ściągnąć klikając w poniższy przycisk
    ''')
 
    with open("docs/Pomorski Czarodziej 2024 - Regulamin.pdf", "rb") as file:
        st.download_button(
            label="Regulamin konkursu",
            data=file,
            file_name='Pomorski Czarodziej 2024 - Regulamin.pdf',
            mime='application/pdf',
)    

with training:
    groups = get_data("editions", {"public": {"$eq": True}})
    groups_names = [group["name"] for group in groups]
    tabs = st.tabs(groups_names)
    # Add tab
    for element in zip(groups, tabs):
        element[0]["tab"] = element[1]

    # Editions
    for group in groups:
        with group["tab"]:
            tasks = get_data("tasks", {"edition": {"$eq": group["name"]}})

            col1, col2 = st.columns([1, 2])
            with col1:
                task_name = st.selectbox(
                    'Wybierz zadanie', [task["name"] for task in tasks], label_visibility="collapsed")
                task = next(filter(lambda x: x["name"] == task_name, tasks))
                st.markdown(f"### {task_name}")
                st.write(task["description"])

            with col2:
                code = task["initial-code"]
                editor_buttons = [{
                    "name": "Uruchom",
                    "feather": "Play",
                    "primary": True,
                    "hasText": True,
                    "showWithIcon": True,
                    "commands": ["submit"],
                    "style": {"bottom": "0.44rem", "right": "0.4rem"},
                    "alwaysOn": True
                }]
                editor_response = code_editor(
                    code, key=group["name"]+task["name"]+"_editor", height=[10, 20], buttons=editor_buttons)

                if editor_response['type'] == "submit":
                    run_code(task, editor_response["text"])