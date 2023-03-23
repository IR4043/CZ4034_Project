import streamlit as st
from header_design import colored_header

st.set_page_config(layout="wide")
with open("./styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

colored_header(label="Crawler Module", color_name="red-70")
st.sidebar.header("")
st.subheader("Crawling Function")

button = st.button("Start Crawling", disabled=False)

