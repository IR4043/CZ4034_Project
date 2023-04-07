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


def display_card(row):
    st.write(f"""
    <div class="card">
        <div class="card-title">
            {"Title: " + row['title']}
        </div>
        <div class="card-text">
            {"Rating Score: " + str(row['rating'])}
            <br/>
            {"Review Date: " + str(row['reviewDate'])}
        <div class ="card-text">
            {"Description: " + str(row['reviewDescription'])}
        </div>    
        <div class="button-container">
            <a class="read-more" href="/Review?index={row['id']}" target="_self">
                Read More
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_data(data):
    row_limit = 3
    columns = st.columns(row_limit)
    for i, result in enumerate(data):
        with columns[i % row_limit]:
            display_card(result)


def auto_complete(searchterm: str) -> List[str]:
    if not searchterm:
        return []
    time.sleep(0.5)
    suggested_terms = requests.get(f"http://127.0.0.1:5000/suggest/{searchterm}").json()
    return suggested_terms


def fetch_results(size, color, sp, pg, sentiment, page=1):
    if size == "" and color == "" and sp == "" and pg == "" and sentiment == "":
        pack_data = {
            "page": page
        }
        response = requests.post("http://127.0.0.1:5000/test_query", json=pack_data)
    else:
        pack_data = {
            "size": size,
            "color": color,
            "service_provider": sp,
            "product_grade": pg,
            "critic": sentiment,
            "page": page
        }
        response = requests.post("http://127.0.0.1:5000/facet_query", json=pack_data)

    response_json = response.json()
    response_docs = response_json["response"]["docs"]
    response_time = float(response_json["time_taken"])
    response_time_string = " ({:.2f}s)".format(response_time)
    response_num_found = response_json["response"]["numFound"]
    search_statistics = "About " + str(response_num_found) + " results" + response_time_string
    st.session_state["statistics"] = search_statistics
    st.session_state["response"] = response_docs
    st.session_state["count"] = response_num_found


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

with st.expander("Charts and Word Cloud"):
    st.write("Works In Progress")

text_search = st_searchbox(label="Search Bar",
                           search_function=auto_complete,
                           placeholder="Search Reviews...",
                           clear_on_submit=False,
                           clearable=True)
# text_search = st.text_input(label="Search Bar", label_visibility="collapsed", placeholder="Search")

form1, form2, form3, form4, form5, form6 = st.columns([1, 1, 1, 1, 1, 1])

with form1:
    size_d = st.selectbox(label="Size", options=["", "64GB", "128GB", "256GB", "512GB"])

with form2:
    color_d = st.selectbox(label="Color", options=["", "Black", "Blue", "Coral", "Gold", "Green", "Midnight Green",
                                                   "Purple", "Red", "Silver", "Space Gray", "White", "Yellow"])

with form3:
    sp_d = st.selectbox(label="Service Provider",
                        options=["", "AT&T", "GSM Carrier", "Sprint", "T-Mobile", "Unlocked",
                                 "Verizon"])
with form4:
    pg_d = st.selectbox(label="Product Grade", options=["", "Renewed", "Renewed Premium"])

with form5:
    sen_d = st.selectbox(label="Sentiment Of Review", options=["", "Positive", "Neutral", "Negative"])

with form6:
    st.markdown('<div class="space-down"></div>', unsafe_allow_html=True)
    button = st.button("Submit", disabled=False, use_container_width=True)

body1, body2 = st.columns([1, 4])

with body1:
    match color_d:
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
    page_menu = st.columns((4.5, 1, 1, 1))
    current_page = 0
    total_pages = 1
    if "page" not in st.session_state:
        st.session_state["page"] = 1
    with page_menu[0]:
        st.subheader("Search Results")

    if button:
        fetch_results(size_d, color_d, sp_d, pg_d, sen_d)
        st.write(st.session_state["statistics"])
        st.session_state['page'] = 1
        display_data(st.session_state["response"])
        total_pages = (st.session_state["count"] // 9) + 1

    elif 'response' in st.session_state:
        st.write(st.session_state["statistics"])
        display_data(st.session_state["response"])
        total_pages = (st.session_state["count"] // 9) + 1

    else:
        st.write("No Results Found")
        total_pages = 1

    with page_menu[1]:
        print(st.session_state['page'])
        decrement_button = st.button("Previous Page", key="Previous", disabled=(st.session_state['page'] == 1))

    with page_menu[3]:
        print(st.session_state['page'])
        increment_button = st.button("Next Page", key="Next", disabled=(st.session_state['page'] == total_pages))

    if decrement_button and st.session_state["page"] > 1:
        st.session_state['page'] -= 1
        fetch_results(size_d, color_d, sp_d, pg_d, sen_d, st.session_state["page"])
        st.experimental_rerun()

    if increment_button and st.session_state["page"] <= total_pages:
        st.session_state['page'] += 1
        fetch_results(size_d, color_d, sp_d, pg_d, sen_d, st.session_state["page"])
        st.experimental_rerun()

    with page_menu[2]:
        st.markdown(f"<div class='space-down2'>Page {st.session_state['page']} of {total_pages}</div>",
                    unsafe_allow_html=True)
