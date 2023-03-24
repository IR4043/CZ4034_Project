import streamlit as st
from header_design import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
with open("./styles/style.css") as source_des:
    st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)


def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Crawler", "Search"],  # required
            icons=["house", "book", "search"],  # optional
            menu_icon="cast",  # optional
            default_index=1,  # optional
        )
    return selected


st.sidebar.markdown('<p class="sidebar-title">SELECT MODULES</p>', unsafe_allow_html=True)
selected = streamlit_menu()
if selected == "Search":
    switch_page("Search")
if selected == "Home":
    switch_page("Home")

colored_header(label="Crawler Module", color_name="red-70")
st.sidebar.header("")
st.subheader("Crawling Function")

button = st.button("Start Crawling", disabled=False)
