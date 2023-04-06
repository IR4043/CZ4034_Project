import streamlit as st
from streamlit_extras.switch_page_button import switch_page

body2_design = """
<div>
    <h6><b>Id: {}</b></h6>
    <h4><b>Ratings: {}</b></h4>
    <h4><b>Variants: {}, {}</b></h4>
    <h4><b>Visit the Offical Website: <a href={}>Link</a></b></h4>
    <h4><b>{}</h4>
    <h4><b>From: {}</b></h4>
</div>
"""

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

with open("styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

query_params = st._get_query_params()
Id = query_params.get("index", [None])[0]
new_label = str(Id)

gold = "https://m.media-amazon.com/images/I/612hfh4g1jL._AC_SL1000_.jpg"
green = "https://m.media-amazon.com/images/I/61IWAlDU-xL._AC_SL1000_.jpg"
silver = "https://m.media-amazon.com/images/I/71SNCEmiscL._AC_SL1500_.jpg"
space_gray = "https://m.media-amazon.com/images/I/51UnWftDvAL._AC_SL1112_.jpg"

# get values
asin = "B08BHHSB6M"
ratings = str(5)

variant = "Size: 256GBColor: Midnight GreenService Provider: UnlockedProduct grade: Renewed Premium"
size_index = variant.find("Size: ") + len("Size: ")
color_index = variant.find("Color: ") + len("Color: ")
size = str(variant[size_index:variant.find("Color:")].strip())
color = str(variant[color_index:variant.find("Service Provider:")].strip())

url = "https://www.amazon.com/gp/customer-reviews/R113JAUTA7B9WY/ref=cm_cr_arp_d_rvw_ttl?ie=UTF8&ASIN=B08BHHSB6M"
reviewed = "Reviewed in the United States on February 3, 2022"
country = "United States"
title = "It does not come with a fast charger"
desc = "I like the fone so far but the charger that it shipped with does not work. I thought I would be getting " \
       "a fast charger since it is the pro version"

back_btn = st.button("Back To Search", disabled=False)
if back_btn:
    switch_page("Search")

body1, body2 = st.columns([2, 2])

with body1:
    st.markdown('<img src={} style="padding:20px; height:70%; width:70%;">'.format(space_gray), unsafe_allow_html=True)

with body2:
    st.markdown(body2_design.format(new_label, ratings, size, color, url, reviewed, country), unsafe_allow_html=True)

    with st.expander(title):
        st.write("Description:" + desc)
