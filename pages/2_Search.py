import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from streamlit_searchbox import st_searchbox
import time
from typing import List


def streamlit_menu():
    bar_menu = option_menu(
        menu_title=None,
        options=["Home", "Crawler", "Search"],  # required
        icons=["house", "book", "search"],  # optional
        menu_icon="cast",  # optional
        default_index=2,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding-top": "10px", "margin": "20px", "min-height": "80px", "background-color": "#FFFFFF"}}
    )
    return bar_menu


def display_card(data):
    st.write(f"""
    <div class="card">
        <div class="card-title">
            {"Id: " + data['id']}
        </div>
        <div class="card-text">
            {"Rating Score: " + str(data['rating'])}
            <br/>
            {"Review Date: " + str(data['reviewDate'])}
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


def auto_complete(searchterm: str) -> List[str]:
    if not searchterm:
        return []
    time.sleep(0.5)
    suggested_terms = requests.get(f"http://127.0.0.1:5000/suggest/{searchterm}").json()
    return suggested_terms


black = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/31PpUfTCiFL._AC_.jpg"
blue = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/61k-gTEf8EL._AC_SL1500_.jpg"
coral = "https://m.media-amazon.com/images/I/61YLDrZHGrL._AC_SL1500_.jpg"
gold = "https://m.media-amazon.com/images/I/612hfh4g1jL._AC_SL1000_.jpg"
green = "https://m.media-amazon.com/images/I/71r0E8xfKcL._AC_SL1500_.jpg"
midnight_green = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/71p2mApMN0L._AC_SL1500_.jpg"
purple = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/61xjLtaQTUL._AC_SL1500_.jpg"
red = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/51phteQ42JL._AC_SL1000_.jpg"
silver = "https://m.media-amazon.com/images/I/71SNCEmiscL._AC_SL1500_.jpg"
space_gray = "https://m.media-amazon.com/images/I/51UnWftDvAL._AC_SL1112_.jpg"
white = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/71jEjOp6D0L._AC_SL1500_.jpg"
yellow = "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/51gyr3c5C9L._AC_SL1000_.jpg"

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
with open("./styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()} </style>", unsafe_allow_html=True)

container = st.container()
with container:
    cols = st.columns([1, 1])
    with cols[0]:
        st.title("Search Module")

    with cols[1]:
        selected = streamlit_menu()
        if selected == "Home":
            switch_page("Home")
        if selected == "Crawler":
            switch_page("Crawler")

    st.markdown('<hr class=hr-1></hr>', unsafe_allow_html=True)

# Clear the query parameters of the website
st._set_query_params()

text_search = st_searchbox(label="",
                           search_function=auto_complete,
                           placeholder="Search Reviews...",
                           clear_on_submit=False,
                           clearable=True)
# text_search = st.text_input(label="Search Bar", label_visibility="collapsed", placeholder="Search")
form1, form2, form3, form4, form5, form6 = st.columns([1, 1, 1, 1, 1, 1])

with form1:
    size_dropdown = st.selectbox(label="Size", options=["", "64GB", "128GB", "256GB", "512GB"])

with form2:
    color_dropdown = st.selectbox(label="Color",
                                  options=["", "Black", "Blue", "Coral", "Gold", "Green", "Midnight Green", "Purple",
                                           "Red",
                                           "Silver", "Space Gray", "White", "Yellow"])

with form3:
    service_provider_dropdown = st.selectbox(label="Service Provider",
                                             options=["", "AT&T", "GSM Carrier", "Sprint", "T-Mobile", "Unlocked",
                                                      "Verizon"])
with form4:
    product_grade_dropdown = st.selectbox(label="Product Grade",
                                          options=["", "Renewed", "Renewed Premium"])

with form5:
    critic_dropdown = st.selectbox(label="Sentiment Of Review", options=["", "Positive", "Neutral", "Negative"])

with form6:
    st.markdown('<div class="space-down"></div>', unsafe_allow_html=True)
    button = st.button("Submit", disabled=False, use_container_width=True)

body1, body2 = st.columns([1, 4])

with body1:
    match color_dropdown:
        case 'Black':
            chosen_color = black
        case 'Blue':
            chosen_color = blue
        case 'Coral':
            chosen_color = coral
        case 'Gold':
            chosen_color = gold
        case 'Green':
            chosen_color = green
        case 'Midnight Green':
            chosen_color = midnight_green
        case 'Purple':
            chosen_color = purple
        case 'Red':
            chosen_color = red
        case 'Silver':
            chosen_color = silver
        case 'Space Gray':
            chosen_color = white
        case 'Yellow':
            chosen_color = yellow
        case _:
            chosen_color = gold

    st.markdown('<img src={} style="height:70%; width:70%;">'.format(chosen_color), unsafe_allow_html=True)

with body2:
    st.subheader("Search Results")

    if button:
        if size_dropdown == "" and color_dropdown == "" and service_provider_dropdown == "" and product_grade_dropdown \
                == "" and critic_dropdown == "":
            response = requests.get("http://127.0.0.1:5000/test_query")
            response_json = response.json()
            response_docs = response_json["response"]["docs"]
            response_time = float(response_json["time_taken"])
            response_time_string = "Search Time: ({:.2f}s)".format(response_time)
            st.write(response_time_string)
            display_data(response_docs)
        else:
            pack_data = {
                "size": size_dropdown,
                "color": color_dropdown,
                "service_provider": service_provider_dropdown,
                "product_grade": product_grade_dropdown,
                "critic": critic_dropdown
            }
            response = requests.post("http://127.0.0.1:5000/facet_query", json=pack_data)
            print(response.json())
            # response_docs = response_json["response"]["docs"]
            # response_time = float(response_json["time_taken"])
            # response_time_string = "Search Time: ({:.2f}s)".format(response_time)
            # st.write(response_time_string)
            # display_data(response_docs)


    elif 'response' in st.session_state:
        json_data = st.session_state["response"]
        display_data(json_data)
