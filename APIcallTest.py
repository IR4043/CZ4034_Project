import requests

url = "http://localhost:8983/solr/amazon_iphone/spell?"

query = "rd phne"

params = {
    "spellcheck.q": query,
    "rows": 5,
    "spellcheck" : "true",
    "spellcheck.collate" : "true",
    "df" : "reviewDescription"
}

response = requests.get(url, params=params)

wordToReplace = {}

if len(response.json()["spellcheck"]["collations"]) > 0:
    query = response.json()["spellcheck"]["collations"][1]["collationQuery"]

else:
    for i in range(0, len(response.json()["spellcheck"]["suggestions"]), 2):
        wordToReplace[response.json()["spellcheck"]["suggestions"][i]] = [response.json()["spellcheck"]["suggestions"][i + 1]][0]["suggestion"][0]["word"]

    for i in wordToReplace:
        query = query.replace(i, wordToReplace[i])



#query commands:
# for spell check : http://localhost:8983/solr/iphone_review/spell?spellcheck.q=dilivery phne&spellcheck=true&spellcheck.collate=true
# for suggester : http://localhost:8983/solr/iphone_review/suggest?suggest=true&suggest.q="battery"
# for MLT : http://localhost:8983/solr/iphone_review/mlt?q=reviewDescription:"bad phone"&mlt.boost=true