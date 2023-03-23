import streamlit as st
from header_design import colored_header

st.set_page_config(layout="wide")
with open("styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

colored_header(
    label="Information Retrieval Project Group-16",
    color_name="red-70"
)
st.sidebar.header("")

st.subheader("Introduction")
st.write("This Project will be focused on the reviews of the Apple IPhone models from the Amazon Store.")
st.title("Modules")
st.subheader("Crawler")
st.write("The Crawler Module helps us to crawl the data using our API keys to gather data from the Amazon Store on "
         "the Reviews of the IPhone Models. In cases of any new data, this will allow us to update the indexer, "
         "with the new incremental indexing shown.")
st.subheader("Search")
st.write("The Search Module presents the user with five queries, the user can choose either of the five queries to be "
         "searched. The results and speed of the query will be displayed.")
