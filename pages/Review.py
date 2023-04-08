import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import requests

body2_design = """
<div>
    <h6><b>Id: {}</b></h6>
    <h4><b>Ratings: {}</b></h4>
    <h4><b>Variant: {}, {}, {}, {}</b></h4>
    <h4><b>Visit the Offical Website: <a href={}>Link</a></b></h4>
    <h4><b>{}</h4>
    <h4><b>Product Asin: {}</b></h4>
    <h4><b>Review: </b></h4>
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

color_dict = {
    "Black": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/31PpUfTCiFL._AC_.jpg",
    "Blue": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/61k-gTEf8EL._AC_SL1500_.jpg",
    "Coral": "https://m.media-amazon.com/images/I/61YLDrZHGrL._AC_SL1500_.jpg",
    "Gold": "https://m.media-amazon.com/images/I/612hfh4g1jL._AC_SL1000_.jpg",
    "Green": "https://m.media-amazon.com/images/I/71r0E8xfKcL._AC_SL1500_.jpg",
    "Midnight Green": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/71p2mApMN0L._AC_SL1500_"
                      ".jpg",
    "Purple": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/61xjLtaQTUL._AC_SL1500_.jpg",
    "Red": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/51phteQ42JL._AC_SL1000_.jpg",
    "Silver": "https://m.media-amazon.com/images/I/71SNCEmiscL._AC_SL1500_.jpg",
    "Space Gray": "https://m.media-amazon.com/images/I/51UnWftDvAL._AC_SL1112_.jpg",
    "White": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/71jEjOp6D0L._AC_SL1500_.jpg",
    "Yellow": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/51gyr3c5C9L._AC_SL1000_.jpg"
}


suggested_terms = requests.get(f"http://127.0.0.1:5000/fetch_record/{Id}").json()
record = suggested_terms["response"]["docs"][0]

id_label = record['id']
asin = record["productAsin"]
ratings = record["rating"]
size = record["size"]
color = record["color"]
service_provider = record["service_provider"]
product_grade = record["product_grade"]
review_title = record["title"]
review_description = record["reviewDescription"]
review_date = record["reviewDate"]
review_link = record["review_link"]
image_link = record["image_links"]


back_btn = st.button("Back To Search", disabled=False)
if back_btn:
    switch_page("Search")

body1, body2 = st.columns([2, 2])

with body1:
    st.markdown('<img src={} style="padding:20px; height:60%; width:60%;">'.format(color_dict[color]), unsafe_allow_html=True)

with body2:
    st.markdown(body2_design.format(id_label, ratings, size, color, service_provider, product_grade, review_link,
                                    review_date, asin), unsafe_allow_html=True)

    with st.expander(review_title):
        st.write("Description: " + review_description)
