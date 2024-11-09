import streamlit as st

from code_editor import code_editor
from utils.runner import display_run_result, run_code
from utils.navbar import display_navbar
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

pc = st.get_option('theme.primaryColor')
bc = st.get_option('theme.backgroundColor')
sbc = st.get_option('theme.secondaryBackgroundColor')
tc = st.get_option('theme.textColor')

display_navbar()

_, center, _ = st.columns([1, 5, 1])
with center:
    st.title("Hello World! 🌎")
    left, right = st.columns([4, 6])

    with left:
        editor_buttons = [{
            "name": "Uruchom Program",
            "feather": "Play",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0.44rem", "right": "0.4rem"},
            "alwaysOn": True
        }]

        editor_response = code_editor(
            "print('Hello World!')", key="_frontpage_editor", height=[10, 20], buttons=editor_buttons)
        if editor_response['type'] == "submit":
            result = run_code(editor_response["text"], "")
            display_run_result(result)

    with right:
        with stylable_container(key="generated_page", css_styles=f"""
                        {{
                            background-color: {sbc};
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            div {{
                                width: 90%;
                            }}
                        }}
                        """):
            st.markdown("""
            ### Cześć, młodzi programiści! 👋
            Zapraszamy Was do świata programowania, gdzie wszystko zaczyna się od magicznego :rainbow[**Hello World**]. To pierwsze kroki, które prowadzą do tworzenia gier, aplikacji i wszystkiego, co tylko sobie wymarzycie. Nasz konkurs to świetna okazja, by spróbować swoich sił i zobaczyć, jakie cuda można wyczarować z kodu. Dołączcie do nas, rozwijając swoje umiejętności, kreatywność i pracę zespołową.
            """)

    # divider()
    
    st.title("Pomorski Czarodziej")
    st.markdown("Nasz konkurs jest skierowany do uczniów szkół podstawowych z pomorza. Wszystkie informacje o tegorocznej edycji możecie znaleźć w zakładce **📰 Aktualności**.")
    
    # st.divider()
    left, center, right = st.columns([3, 3, 3])

    with left:
        with stylable_container(key="generated_page_2", css_styles=f"""
                        {{
                            background-color: {sbc};
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            div {{
                                width: 90%;
                            }}
                        }}
                        """):
            st.page_link(
                "src/ide.py", label="Programuj!", icon="⌨️", use_container_width=False)
            st.markdown("""
                        Aby ułatwić Wam dostęp do programowania, nasza strona udostępnia gotowe środowisko programistyczne języka Python w zakładce **Programuj!**
                        """)

    with center:
        with stylable_container(key="generated_page_3", css_styles=f"""
                        {{
                            background-color: {sbc};
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            div {{
                                width: 90%;
                            }}
                        }}
                        """):
            st.page_link(
                "src/training.py", label="Zbiór Zadań", icon="📚", use_container_width=False)
            st.markdown("""
                        Aby ułatwić Wam przygotowanie do konkursu, w zakładce **Zbiór Zadań** przygotowaliśmy dla Was zadania z poprzednich edycji. Wszystkie zadania są automatycznie sprawdzane przez nasz serwis, więc śmiało możecie sprawdzić swoją wiedzę 🎯.
                        """)

    with right:
        with stylable_container(key="generated_page_4", css_styles=f"""
                        {{
                            background-color: {sbc};
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            div {{
                                width: 90%;
                            }}
                        }}
                        """):
            st.page_link(
                "src/competition.py", label="Konkurs", icon="📝", use_container_width=False)
            st.markdown("""
                        W dniu konkursu zakładka **Konkurs** będzie otwarta dla wszystkich chętnych! Po wprowadzeniu identyfikatora otrzymanego od nauczyciela będziecie mieli godzinę na rozwiązanie kilku zadań podobnych do tych ze *Zbioru Zadań*. Powodzenia!
                        """)

    st.markdown('''
        ## Regulamin
        Regulamin konkursu na rok 2025 możecie pobrać, klikając w poniższy przycisk.
    ''')

    with open("docs/Pomorski Czarodziej 2025 - Regulamin.pdf", "rb") as file:
        st.download_button(
            label="Regulamin konkursu",
            data=file,
            file_name='Pomorski Czarodziej 2025 - Regulamin.pdf',
            mime='application/pdf')
