import streamlit as st
from header_design import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_multipage import MultiPage

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
with open("../styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)
    # st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

st.sidebar.header("")


query_params = st._get_query_params()
Id = query_params.get("index", [None])[0]
new_label = "Review Id: " + str(Id)

colored_header(label=new_label, color_name="red-70")
st.subheader("Country")
st.write("United States")
st.subheader("Date")
st.write("2023-03-11T00:00:00Z")
st.subheader("Position")
st.write(str(370))
st.subheader("Description")
with st.expander("Review Title: It does not come with a fast charger"):
    st.write("Description: " + "I like the fone so far but the charger that it shipped with does not work. I thought "
                               "I would be getting a fast charger since it is the pro version")

st.subheader("URL")
st.write("[Review Link]('https://www.amazon.com/gp/customer-reviews/R113JAUTA7B9WY/ref=cm_cr_arp_d_rvw_ttl?ie=UTF8"
         "&ASIN=B08BHHSB6M)")
st.subheader("Reviewed In")
st.write("Reviewed in the United States on February 3, 2022")
st.subheader("Variant")
st.write("Size: 256GBColor: Midnight GreenService Provider: UnlockedProduct grade: Renewed Premium")
st.subheader("")
back_btn = st.button("Back To Search", disabled=False)
if back_btn:
    switch_page("Search")
