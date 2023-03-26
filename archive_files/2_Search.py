import streamlit as st
import requests
from header_design import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu


def display_card(data):
    st.write(f"""
    <div class="card">
        <div class="card-title">
            {"Id: " + data['id']}
        </div>
        <div class="card-text">
            {"Rating Score: " + str(data['ratingScore'])}
            <br/>
            {"Review Date: " + str(data['date'])}
        <div class ="card-text">
            {"Description: " + str(data['reviewDescription'])}
        </div>    
        <div class="button-container">
            <a class="read-more" href="/Review?index={data['id']}" target="_self">
                Read More
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Crawler", "Search"],  # required
            icons=["house", "book", "search"],  # optional
            menu_icon="cast",  # optional
            default_index=2,  # optional
        )
    return selected


def display_data(data):
    row_limit = 3
    columns = st.columns(row_limit)
    if 'response' not in st.session_state:
        st.session_state['response'] = data
    if data is not None:
        for i, result in enumerate(data):
            with columns[i % row_limit]:
                display_card(result)
    else:
        st.write("No Results Found")


st.set_page_config(layout="wide")
with open("../styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)
    st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-title">SELECT MODULES</p>', unsafe_allow_html=True)
selected = streamlit_menu()
if selected == "Crawler":
    switch_page("Crawler")
if selected == "Home":
    switch_page("Home")

# This is to clear the query parameters of the website
st._set_query_params()

colored_header(label="Search Module", color_name="red-70")
st.sidebar.header("")

st.subheader("Select Your Queries")

col1, col2, col3, col4, col5 = st.columns([.09, .09, .09, .09, 1])

with col1:
    query1_btn = st.button("Query 1", disabled=True)
with col2:
    query2_btn = st.button("Query 2", disabled=True)
with col3:
    query3_btn = st.button("Query 3", disabled=True)
with col4:
    query4_btn = st.button("Query 4", disabled=True)
with col5:
    query5_btn = st.button("Query 5", disabled=True)

st.subheader("Search Bar")

text_search = st.text_input(label="Search Bar", label_visibility="collapsed")
button = st.button("Submit", disabled=False)

st.subheader("Search Results")

if 'response' in st.session_state:
    json_data = st.session_state["response"]
    display_data(json_data)

if button:
    response = requests.get("http://127.0.0.1:5000/query1")
    response_json = response.json()
    response_json = response_json["response"]["docs"]
    # st.write(response_json)
    display_data(response_json)
    # row_limit = 3
    # word_limit = 40
    # columns = st.columns(row_limit)
    # if response_json is not None:
    #     for i, result in enumerate(response_json):
    #         with columns[i % row_limit]:
    #             display_card(result)
    # else:
    #     st.write("No Results Found")

# with st.container():
#     st.write("ID: " + str(result['id']))
#     st.write("Rating Score: " + str(result['ratingScore']))
#     st.write("Review Date: " + str(result['date']))
# with st.container():

#     if len(result['reviewDescription']) > word_limit:
#         description_words = result['reviewDescription'].split()
#         limited_words = description_words[:word_limit]
#         limited_desc = ' '.join(limited_words) + "..."
#         st.write(limited_desc)
#     else:
#         st.write(result['reviewDescription'])
