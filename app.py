import json
import requests
from flask import Flask, request, Response
import time

app = Flask(__name__)


@app.route('/test_query', methods=['GET'])
def test_query():
    start = time.time()
    SORL_URL = "http://localhost:8983/solr/amazon_iphone/select?indent=true&q.op=OR&q=rating%3A%204.0&rows=10"
    response = requests.get(SORL_URL)
    end = time.time()
    time_taken = {"time_taken": end - start}
    response_data = response.json()
    response_data.update(time_taken)
    return response_data


@app.route('/update_index', methods=['POST'])
def update_index():
    data_lst = json.loads(request.data)['docs']
    params = {"boost": 1.0, "overwrite": "true", "commitWithin": 1000}
    url = 'http://127.0.0.1:8983/solr/amazon_iphone/update?wt=json'
    headers = {"Content-Type": "application/json"}
    result = requests.post(url, json=data_lst, params=params, headers=headers)
    return Response(result)


@app.route('/suggest/<search_term>', methods=['GET'])
def suggest_terms(search_term):
    query_url = "http://localhost:8983/solr/amazon_iphone/suggest?suggest=true&suggest.dictionary=mySuggester&suggest" \
                ".q="
    query_url += search_term + "&hl=false"
    headers = {"Content-Type": "application/json"}
    result = requests.get(query_url, headers=headers)
    result = result.json()
    result = result["suggest"]["mySuggester"][search_term]["suggestions"]
    terms = []
    for i in result:
        terms.append(i["term"])
    return terms


@app.route('/facet_query', methods=["POST"])
def facet_query():
    data_list = request.get_json()
    facet_fields = {
        "size": data_list["size"],
        "color": data_list["color"],
        "service_provider": data_list["service_provider"],
        "product_grade": data_list["product_grade"],
        "critic": data_list["critic"]
    }

    base_query = "http://localhost:8983/solr/amazon_iphone/select?q=*:*&"
    facet_q = "facet.field"

    if any(facet_fields.values()):
        base_query += "facet=true&"

    for field, value in facet_fields.items():
        if value:
            base_query += f"{facet_q}={field}&fq={field}:{value}&"

    # Remove the last '&' from the base_query
    base_query = base_query.rstrip('&')

    headers = {"Content-Type": "application/json"}
    result = requests.get(base_query, headers=headers)
    result = result.json()
    return result


if __name__ == '__main__':
    app.run()
