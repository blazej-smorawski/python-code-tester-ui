import streamlit as st


def render_front_page(release=True):
    try:
        if not release:
            import streamlit.components.v1 as components
            _component_func = components.declare_component(
                "front_page_component",
                url="http://localhost:3001")
            _component_func(images=["./app/static/pic01.jpg",
                                    "./app/static/pic02.jpg",
                                    "./app/static/pic03.jpg",
                                    "./app/static/pic04.jpg",
                                    "./app/static/pic05.jpg",
                                    "./app/static/pic06.jpg"])
        else:
            from deps.pomorski_czarodziej_components import front_page_component
            front_page_component.front_page_component(images=["./app/static/pic01.jpg",
                                    "./app/static/pic02.jpg",
                                    "./app/static/pic03.jpg",
                                    "./app/static/pic04.jpg",
                                    "./app/static/pic05.jpg",
                                    "./app/static/pic06.jpg"])
    except:
        st.error("Front page could not be loaded!")
