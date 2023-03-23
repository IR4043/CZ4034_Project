import streamlit as st
import requests
from header_design import colored_header


def display_card(data):
    st.write(f"""
    <div class="card">
        <div class="card-title">
            {"ID: " + data['id']}
        </div>
        <div class="card-text">
            {"Rating Score: " + str(data['ratingScore'])}
        </div>
        <div class="card-text">
            {"Review Date: " + str(data['date'])}
        </div>
        <div class="card-text">
            {"Description: " + str(data['reviewDescription'])}
        </div>
    </div>
    """, unsafe_allow_html=True)


st.set_page_config(layout="wide")
with open("./styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

colored_header(label="Search Module", color_name="red-70")
st.sidebar.header("")

st.subheader("Select Your Queries")

col1, col2, col3, col4, col5 = st.columns([.09, .09, .09, .09, 1])

with col1:
    query1_btn = st.button("Query 1")
with col2:
    query2_btn = st.button("Query 2")
with col3:
    query3_btn = st.button("Query 3")
with col4:
    query4_btn = st.button("Query 4")
with col5:
    query5_btn = st.button("Query 5")

st.subheader("Search For Results")

text_search = st.text_input(label="Search Bar", label_visibility="collapsed")
button = st.button("Submit", disabled=False)

st.subheader("Search Results")

if button:
    response = requests.get("http://127.0.0.1:5000/query1")
    response_json = response.json()
    response_json = response_json["response"]["docs"]
    # st.write(response_json)
    row_limit = 3
    word_limit = 40
    columns = st.columns(row_limit)
    if response_json is not None:
        for i, result in enumerate(response_json):
            with columns[i % row_limit]:
                display_card(result)
    else:
        st.write("No Results Found")

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
