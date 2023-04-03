import requests

url = "http://localhost:8983/solr/iphone_review/spell?spellcheck.q=repar dilivery phne&spellcheck=true&spellcheck.collate=true"

params = {
    "q": "id:111",
    "rows": 5
}

query = "repar dilivery phne"

response = requests.get(url, params=params)

wordToReplace = {}


for i in range(0, len(response.json()["spellcheck"]["suggestions"]), 2):
    wordToReplace[response.json()["spellcheck"]["suggestions"][i]] = [response.json()["spellcheck"]["suggestions"][i + 1]][0]["suggestion"][0]["word"]
    
for i in wordToReplace:
    query = query.replace(i, wordToReplace[i])

print(query)

url = "http://localhost:8983/solr/iphone_review/mlt?q=reviewDescription:'" + query + "'&mlt.boost=true&fl=reviewDescription"

response = requests.get(url, params=params)

print(url)


#query commands:
# for spell check : http://localhost:8983/solr/iphone_review/spell?spellcheck.q=dilivery phne&spellcheck=true&spellcheck.collate=true
# for suggester : http://localhost:8983/solr/iphone_review/suggest?suggest=true&suggest.q="battery"
# for MLT : http://localhost:8983/solr/iphone_review/mlt?q=reviewDescription:"bad phone"&mlt.boost=true