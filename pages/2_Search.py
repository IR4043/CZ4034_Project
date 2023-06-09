import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
import time
from st_keyup import st_keyup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json


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


def auto_complete(search_term):
    if not search_term:
        return []
    time.sleep(0.5)
    suggested_terms = requests.get(f"http://127.0.0.1:5000/suggest/{search_term}").json()
    return suggested_terms


def fetch_results(search_term, data_dict, q_type, page=1):
    params = data_dict
    params["page"] = page
    if search_term:
        st.session_state["mlt"] = 1
        st.session_state["search_term"] = search_term
    else:
        st.session_state["search_term"] = ""

    params["search_term"] = search_term
    if not q_type:
        print("Invoked 1")
        response = requests.post("http://127.0.0.1:5000/general_query", json=pack_data)
        if search_term:
            correction = requests.get(f"http://127.0.0.1:5000/spell_check/{search_term}").json()
            if correction["spellcheck"]:
                st.session_state["spellcheck"] = correction["spellcheck"]
            else:
                st.session_state["spellcheck"] = ""
    else:
        print("Invoked 2")
        response = requests.post("http://127.0.0.1:5000/mlt_query", json=pack_data)
        st.session_state["mlt"] = 0

    response_json = response.json()
    response_docs = response_json["response"]["docs"]
    response_time = float(response_json["time_taken"])
    response_time_string = " ({:.4f}s)".format(response_time)
    response_num_found = response_json["response"]["numFound"]
    search_statistic = "About " + str(response_num_found) + " results" + response_time_string
    st.session_state["statistics"] = search_statistic

    st.session_state["response"] = response_docs
    st.session_state["count"] = response_num_found
    if page == 1:
        if response_json["text"] != "":
            st.session_state["wordcloud"] = response_json["text"]

        if response_json["facet"] != "":
            st.session_state["facet"] = json.loads(response_json["facet"])

    if response_num_found == 0:
        st.session_state["mlt"] = 0

    st.experimental_rerun()


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

if "wordcloud" not in st.session_state:
    st.session_state["wordcloud"] = "default"
if "default_word" not in st.session_state:
    st.session_state["default_word"] = ""
if "spellcheck" not in st.session_state:
    st.session_state["spellcheck"] = ""
if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""
if "facet" not in st.session_state:
    st.session_state["facet"] = ""

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

expander_placeholder = st.empty()
expander_charts = expander_placeholder.expander("Charts and Word Cloud")

text_search = st_keyup("Search", debounce=100)

if text_search != st.session_state["last_input"]:
    st.session_state["last_input"] = text_search
    suggestions = auto_complete(text_search)
    st.write(suggestions)
else:
    suggestions = []

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
    sen_d = st.selectbox(label="Sentiment Of Review", options=["", "Positive", "Negative"])

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

# This is for button session state to make it appear or not
if "mlt" not in st.session_state:
    st.session_state["mlt"] = 0

# This to tell the server what type of query to use. Default should always be set to 0
if "mlt_query" not in st.session_state:
    st.session_state["mlt_query"] = 0

with body2:
    page_menu = st.columns((4.5, 1, 1, 1))
    current_page = 0
    total_pages = 1
    if "page" not in st.session_state:
        st.session_state["page"] = 1
    with page_menu[0]:
        st.subheader("Search Results")

    more_like_this_button = None
    spell_check_button = None
    statistics = st.empty()
    more_like_this = st.empty()
    spell_check = st.empty()

    pack_data = {
        "size": size_d,
        "color": color_d,
        "service_provider": sp_d,
        "product_grade": pg_d,
        "sentiment": sen_d
    }

    if button:
        st.session_state["mlt_query"] = 0
        st.session_state["spellcheck"] = ""
        fetch_results(text_search, pack_data, st.session_state["mlt_query"])
        statistics.write(st.session_state["statistics"])
        st.session_state['page'] = 1
        # if text_search:
        #     st.session_state["mlt"] = 1
        #     more_like_this_button = more_like_this.button("More Results Like This")
        # # display_data(st.session_state["response"])
        # total_pages = (st.session_state["count"] // 9) + 1

    elif 'response' in st.session_state:
        statistics.write(st.session_state["statistics"])
        display_data(st.session_state["response"])
        total_pages = (st.session_state["count"] // 9) + 1
        if st.session_state["mlt"] == 1:
            more_like_this_button = more_like_this.button("More Results Like This")

    else:
        st.write("No Results Found")
        total_pages = 1

    with page_menu[1]:
        decrement_button = st.button("Previous Page", key="Previous", disabled=(st.session_state['page'] == 1))

    with page_menu[3]:
        increment_button = st.button("Next Page", key="Next", disabled=(st.session_state['page'] == total_pages))

    if decrement_button and st.session_state["page"] > 1:
        st.session_state['page'] -= 1
        fetch_results(text_search, pack_data, st.session_state["mlt_query"], st.session_state["page"])

    if increment_button and st.session_state["page"] <= total_pages:
        st.session_state['page'] += 1
        fetch_results(text_search, pack_data, st.session_state["mlt_query"], st.session_state["page"])

    with page_menu[2]:
        st.markdown(f"<div class='space-down2'>Page {st.session_state['page']} of {total_pages}</div>",
                    unsafe_allow_html=True)

    if more_like_this_button:
        st.session_state["mlt_query"] = 1
        st.session_state["page"] = 1
        fetch_results(text_search, pack_data, st.session_state["mlt_query"])

    if st.session_state["spellcheck"]:
        spell_check_button = spell_check.button("Do you mean: " + "'" + st.session_state["spellcheck"] + "'")

    if spell_check_button:
        st.session_state["mlt_query"] = 0
        st.session_state['page'] = 1
        fetch_results(st.session_state["spellcheck"], pack_data, st.session_state["mlt_query"])

with expander_charts:
    fig, ax = plt.subplots(2, 3, figsize=(10, 6), tight_layout=True)

    wordcloud = WordCloud(background_color="white").generate(st.session_state["wordcloud"])

    ax[0, 0].imshow(wordcloud, interpolation="bilinear")
    ax[0, 0].set_title("Word Cloud")
    ax[0, 0].axis('off')

    if "size" in st.session_state["facet"]:
        size_label = []
        size_count = []
        for i in range(0, len(st.session_state["facet"]["size"]), 2):
            if st.session_state["facet"]["size"][i + 1] > 0:
                size_label.append(st.session_state["facet"]["size"][i])
                size_count.append(st.session_state["facet"]["size"][i + 1])

        fSizeLabel = []
        for i in range(0, len(size_label)):
            fSizeLabel.append(size_label[i] + " " + str(round(size_count[i] / sum(size_count) * 100, 2)) + "% ")

        ax[1, 0].pie(size_count, labels=None, autopct='', startangle=90, textprops={'fontsize': 6})
        ax[1, 0].legend(fSizeLabel, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=5)
        ax[1, 0].set_title("Size", loc="right")

    if "service_provider" in st.session_state["facet"]:
        sp_label = []
        sp_count = []
        for i in range(0, len(st.session_state["facet"]["service_provider"]), 2):
            if st.session_state["facet"]["service_provider"][i + 1] > 0:
                sp_label.append(st.session_state["facet"]["service_provider"][i])
                sp_count.append(st.session_state["facet"]["service_provider"][i + 1])

        fSPlabel = []
        for i in range(0, len(sp_label)):
            fSPlabel.append(sp_label[i] + " " + str(round(sp_count[i] / sum(sp_count) * 100, 2)) + "% ")

        ax[0, 1].pie(sp_count, labels=None, autopct='', startangle=90, textprops={'fontsize': 6})
        ax[0, 1].legend(fSPlabel, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=5)
        ax[0, 1].set_title("Service Provider", loc="right")

    if "product_grade" in st.session_state["facet"]:
        pg_label = []
        pg_count = []
        for i in range(0, len(st.session_state["facet"]["product_grade"]), 2):
            if st.session_state["facet"]["product_grade"][i + 1] > 0:
                pg_label.append(st.session_state["facet"]["product_grade"][i])
                pg_count.append(st.session_state["facet"]["product_grade"][i + 1])

        fPGlabel = []
        for i in range(0, len(pg_label)):
            fPGlabel.append(pg_label[i] + " " + str(round(pg_count[i] / sum(pg_count) * 100, 2)) + "% ")

        ax[1, 1].pie(pg_count, labels=None, autopct='', startangle=90, textprops={'fontsize': 6})
        ax[1, 1].legend(fPGlabel, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=5)
        ax[1, 1].set_title("Quality", loc="right")

    if "color" in st.session_state["facet"]:
        c_label = []
        c_count = []
        for i in range(0, len(st.session_state["facet"]["color"]), 2):
            if st.session_state["facet"]["color"][i + 1] > 0:
                c_label.append(st.session_state["facet"]["color"][i])
                c_count.append(st.session_state["facet"]["color"][i + 1])

        fClabel = []
        for i in range(0, len(c_label)):
            fClabel.append(c_label[i] + " " + str(round(c_count[i] / sum(c_count) * 100, 2)) + "% ")

        ax[0, 2].pie(c_count, labels=None, autopct='', startangle=90, textprops={'fontsize': 6})
        ax[0, 2].set_title("color", loc="right")
        ax[0, 2].legend(fClabel, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=5)

    if "sentiment" in st.session_state["facet"]:
        s_label = []
        s_count = []
        for i in range(0, len(st.session_state["facet"]["sentiment"]), 2):
            if st.session_state["facet"]["sentiment"][i + 1] > 0:
                s_label.append(st.session_state["facet"]["sentiment"][i])
                s_count.append(st.session_state["facet"]["sentiment"][i + 1])

        sentiment_label = []
        for i in range(0, len(s_label)):
            sentiment_label.append(s_label[i] + " " + str(round(s_count[i] / sum(s_count) * 100, 2)) + "% ")

        ax[1, 2].pie(s_count, labels=None, autopct='', startangle=90, textprops={'fontsize': 6})
        ax[1, 2].set_title("sentiment", loc="right")
        ax[1, 2].legend(sentiment_label, loc="center left", bbox_to_anchor=(-0.1, 1.), fontsize=5)

    st.pyplot(plt)
