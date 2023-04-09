import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
import time
from st_keyup import st_keyup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Create some sample text
text = ""

response = requests.get(f'http://localhost:8983/solr/UpdatedData/select?defType=dismax&hl.fl=reviewDescription&mm=3&q.op=OR&q=64%20gb%20phone&qf=reviewDescription&spellcheck.build=true&spellcheck=true&fl=reviewDescription&rows=2147483647').json()

print(response['response']['docs'])

for i in response['response']['docs']:
    text = text + "," + i['reviewDescription']


# Create and generate a word cloud image:
wordcloud = WordCloud(background_color='white').generate(text)
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
st.pyplot(plt)


