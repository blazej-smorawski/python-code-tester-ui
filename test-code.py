import streamlit as st

from code_editor import code_editor
from utils.frontpage import render_front_page
from utils.runner import display_run_result, run_code
from utils.navbar import display_navbar
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container

_RELEASE = True

pc = st.get_option('theme.primaryColor')
bc = st.get_option('theme.backgroundColor')
sbc = st.get_option('theme.secondaryBackgroundColor')
tc = st.get_option('theme.textColor')

display_navbar()

_, center, _ = st.columns([1, 5, 1])
with center:
    render_front_page(_RELEASE)
    
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
            "print('Hello world!')", key="_frontpage_editor", height=[10, 20], buttons=editor_buttons)
        if editor_response['type'] == "submit":
            result = run_code(editor_response["text"], "")
            display_run_result(result)

    with right:
        with stylable_container(key="generated_page", css_styles=f"""
                        {{
                            background-color: {sbc};
                            z-index: 999;
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            border-radius: 5px;
                        }}
                        """):
            st.markdown("""
            ### Lorem
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam libero elit, pellentesque eget efficitur sed, bibendum et nulla. Sed faucibus dolor lectus, pretium gravida eros imperdiet in. Duis pretium ac metus sed iaculis. Proin id molestie elit. Curabitur fermentum, leo ut porttitor congue, odio felis rutrum erat, vel tempor sem velit in nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Duis porta turpis a egestas lobortis. Phasellus interdum neque a ipsum ultrices facilisis. Duis ligula erat, blandit ut convallis sed, vulputate non neque. Curabitur eu malesuada elit. In ac massa at neque placerat dignissim. Vestibulum sed ullamcorper est, vestibulum dignissim augue. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse varius ornare lectus in vestibulum.
            """)

    st.divider()
    left, right = st.columns([6, 4])

    with left:
        with stylable_container(key="generated_page_2", css_styles=f"""
                        {{
                            background-color: {sbc};
                            z-index: 999;
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            border-radius: 5px;
                        }}
                        """):
            with st.container(height=300, border=False):
                st.markdown("""
                ### Hello
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam libero elit, pellentesque eget efficitur sed, bibendum et nulla. Sed faucibus dolor lectus, pretium gravida eros imperdiet in. Duis pretium ac metus sed iaculis. Proin id molestie elit. Curabitur fermentum, leo ut porttitor congue, odio felis rutrum erat, vel tempor sem velit in nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Duis porta turpis a egestas lobortis. Phasellus interdum neque a ipsum ultrices facilisis. Duis ligula erat, blandit ut convallis sed, vulputate non neque. Curabitur eu malesuada elit. In ac massa at neque placerat dignissim. Vestibulum sed ullamcorper est, vestibulum dignissim augue. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse varius ornare lectus in vestibulum.
                """)

    with right:
        with stylable_container(key="generated_page_2", css_styles=f"""
                        {{
                            background-color: {sbc};
                            z-index: 999;
                            padding: 10px;
                            border-style: solid;
                            border-width: 1px;
                            border-radius: 5px;
                            border-color: {pc};
                            border-radius: 5px;
                        }}
                        """):
            with st.container(height=300, border=False):
                st.markdown("""
                ### Tak
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam libero elit, pellentesque eget efficitur sed, bibendum et nulla. Sed faucibus dolor lectus, pretium gravida eros imperdiet in. Duis pretium ac metus sed iaculis. Proin id molestie elit. Curabitur fermentum, leo ut porttitor congue, odio felis rutrum erat, vel tempor sem velit in nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Duis porta turpis a egestas lobortis. Phasellus interdum neque a ipsum ultrices facilisis. Duis ligula erat, blandit ut convallis sed, vulputate non neque. Curabitur eu malesuada elit. In ac massa at neque placerat dignissim. Vestibulum sed ullamcorper est, vestibulum dignissim augue.
                """)

    st.markdown('''
        ## Regulamin
        Regulamin konkursu na rok 2024 możesz ściągnąć klikając w poniższy przycisk
    ''')

    with open("docs/Pomorski Czarodziej 2024 - Regulamin.pdf", "rb") as file:
        st.download_button(
            label="Regulamin konkursu",
            data=file,
            file_name='Pomorski Czarodziej 2024 - Regulamin.pdf',
            mime='application/pdf')
