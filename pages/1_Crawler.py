import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from amazon_crawl import scrape
import pandas as pd


def streamlit_menu():
    bar_menu = option_menu(
        menu_title=None,
        options=["Home", "Crawler", "Search"],  # required
        icons=["house", "book", "search"],  # optional
        menu_icon="cast",  # optional
        default_index=1,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding-top": "10px", "margin": "20px", "min-height": "80px", "background-color": "#FFFFFF"}}
    )
    return bar_menu


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
with open("./styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

# Container Class
container = st.container()
with container:
    cols = st.columns([1, 1])
    with cols[0]:
        st.title("Crawler Module")

    with cols[1]:
        selected = streamlit_menu()
        if selected == "Search":
            switch_page("Search")
        if selected == "Home":
            switch_page("Home")

    st.markdown('<hr class=hr-1></hr>', unsafe_allow_html=True)

st.subheader("Crawling Function")
crawl_links = st.text_area(label="Insert Links")
button = st.button("Start Crawling", disabled=False)
default_progress = "Scraping Operation In Progress. Please Wait"
my_bar = st.progress(0, text="")

df = pd.DataFrame(columns=["title", 'rating', 'productAsin', 'reviewDate', 'reviewDescription', 'size', 'color',
                           'service_provider', 'product_grade', 'review_link', 'image_links'])

dataframe_space = st.empty()
incremental_index = st.empty()

dataframe_space.dataframe(df)
incremental_button = incremental_index.button("Update Index")

if button:
    link_list = crawl_links.split(",")
    length_link = len(link_list)
    count = 1
    for i in link_list:
        result = scrape(i)
        for j in result:
            new_row = pd.DataFrame({k: [v] for k, v in j.items()})
            df = pd.concat([df, new_row], ignore_index=True)
        my_bar.progress((count / length_link), text="Scrape Operation for Link " + str(count) + " done.")
        count += 1

    dataframe_space.dataframe(df)
    st.session_state["record_df"] = df

if incremental_button:
    if st.session_state["record_df"].empty:
        st.write("No records to perform incremental updates to index.")
    else:
        st.write("Updating")
        # Write the logic here for MODEL PREDICTION

