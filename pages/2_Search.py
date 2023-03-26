import streamlit as st
import requests
from header_design import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu


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
with open("styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()} </style>", unsafe_allow_html=True)
    st.markdown('<style> ul {display: none;} </style>', unsafe_allow_html=True)

colored_header(label="IPhone Models", color_name="red-70")

st.sidebar.markdown('<p class="sidebar-title">SELECT MODULES</p>', unsafe_allow_html=True)
selected = streamlit_menu()
if selected == "Crawler":
    switch_page("Crawler")
if selected == "Home":
    switch_page("Home")

# This is to clear the query parameters of the website
st._set_query_params()

# st.subheader("Search Bar")
text_search = st.text_input(label="Search Bar", label_visibility="collapsed", placeholder="Search")
form1, form2, form3 = st.columns([2, 2, 1])

# style for horizontal radio button
st.write(
    '<style>div.row-widget.stRadio> div{flex-direction:row;justify-content: center; border:1px dotted red; padding:10px;} </style>',
    unsafe_allow_html=True)

st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{padding-left:2px;}</style>', unsafe_allow_html=True)
with form1:
    selected_size = st.radio('Size:', ('64GB', '256GB', '512GB', 'ALL'), label_visibility='collapsed')

with form2:
    selected_color = st.radio('Color:', ('Gold', 'Midnight Green', 'Silver', 'Space Gray', 'ALL'),
                              label_visibility='collapsed')

with form3:
    button = st.button("Submit", disabled=False)

body1, body2 = st.columns([1, 4])

with body1:
    gold = "https://m.media-amazon.com/images/I/612hfh4g1jL._AC_SL1000_.jpg"
    green = "https://m.media-amazon.com/images/I/61IWAlDU-xL._AC_SL1000_.jpg"
    silver = "https://m.media-amazon.com/images/I/71SNCEmiscL._AC_SL1500_.jpg"
    space_gray = "https://m.media-amazon.com/images/I/51UnWftDvAL._AC_SL1112_.jpg"

    chosen_color = gold  # default color
    if selected_color == 'Gold':
        chosen_color = gold
    elif selected_color == 'Midnight Green':
        chosen_color = green
    elif selected_color == 'Silver':
        chosen_color = silver
    elif selected_color == 'Space Gray':
        chosen_color = space_gray

    st.markdown('<img src={} style="height:70%; width:70%;">'.format(chosen_color), unsafe_allow_html=True)

with body2:
    st.subheader("Search Results")

    if button:
        response = requests.get("http://127.0.0.1:5000/query1")
        response_json = response.json()
        response_json = response_json["response"]["docs"]
        display_data(response_json)

    elif 'response' in st.session_state:
        json_data = st.session_state["response"]
        display_data(json_data)