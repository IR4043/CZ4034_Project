import json
import requests
from flask import Flask, request, Response
import time
from urllib.parse import quote

app = Flask(__name__)


@app.route('/test_query', methods=['POST'])
def test_query():
    SORL_URL = "http://localhost:8983/solr/amazon_iphone/select?indent=true&q.op=OR&q=rating%3A%204.0&"
    data_list = request.get_json()
    page_number = (data_list["page"] - 1) * 9
    SORL_URL += f"start={page_number}&rows=9"
    start = time.time()
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


@app.route('/spell_check/<search_term>', methods=['GET'])
def spell_check(search_term):
    query_url = "http://localhost:8983/solr/amazon_iphone/spell?"
    params = {
        "spellcheck.q": search_term,
        "rows": 5,
        "spellcheck": "true",
        "spellcheck.collate": "true",
        "df": "reviewDescription"
    }
    query = ""
    response = requests.get(query_url, params=params).json()
    if len(response["spellcheck"]["collations"]) > 0:
        query = response["spellcheck"]["collations"][1]["collationQuery"]

    result = {"spellcheck": query}
    return result


@app.route('/fetch_record/<doc_id>', methods=['GET'])
def fetch_record(doc_id):
    query_url = "http://localhost:8983/solr/amazon_iphone/select?"
    query_url += f"q=id:{doc_id}"
    headers = {"Content-Type": "application/json"}
    result = requests.get(query_url, headers=headers).json()
    return result


@app.route('/general_query', methods=["POST"])
def general_query():
    data_list = request.get_json()
    facet_fields = {
        "size": data_list["size"]
    }
    # Declare Variables
    format_service = ""
    format_product = ""
    format_color = ""
    format_sentiment = ""

    # Pre-Processing for category fields
    if data_list["service_provider"]:
        format_service = quote(data_list["service_provider"])
        format_service = "%22" + format_service + "%22"
    if data_list["product_grade"]:
        format_product = quote(data_list["product_grade"])
        format_product = "%22" + format_product + "%22"
    if data_list["color"]:
        format_color = quote(data_list["color"])
        format_color = "%22" + format_color + "%22"
    if data_list["sentiment"]:
        format_sentiment = data_list["sentiment"]
        if format_sentiment != 1:
            format_sentiment = quote(format_sentiment)

    # Adding it to the facet fields dictionary
    facet_fields["service_provider"] = format_service
    facet_fields["product_grade"] = format_product
    facet_fields["color"] = format_color
    facet_fields["sentiment"] = format_sentiment

    base_query = "http://localhost:8983/solr/amazon_iphone/select?"
    if data_list["search_term"]:
        format_search_term = quote(data_list["search_term"])
        base_query += "defType=dismax&q=" + format_search_term + "&mm=1&"
        # Assigning importance to reviewDescription
        base_query += "qf=reviewDescription&"
    else:
        base_query += "q=*:*&"

    count = 0
    for field, value in facet_fields.items():
        if value and count == 0:
            base_query += f"fq={field}:{value} AND "
            count += 1
        elif value:
            base_query += f"{field}:{value} AND "

    base_query = base_query.rstrip(' AND ')

    if count == 1:
        base_query += "&"
        # Call one Query to get all text and facet for data analysis
    text = ""
    facet = ""
    headers = {"Content-Type": "application/json"}
    if data_list["page"] == 1:
        # Facet and Text Counting for Data Analysis
        additional_params = "rows=500&facet=true"
        for field, value in facet_fields.items():
            additional_params += f"&facet.field={field}"
        result = requests.get(base_query + additional_params, headers=headers).json()

        if len(result['response']['docs']) != 0:
            for i in result['response']['docs']:
                text = text + "," + i['reviewDescription']

            if result['facet_counts']['facet_fields']:
                facet = json.dumps(result['facet_counts']['facet_fields'])

    # Adding Page Numbers
    page_number = (data_list["page"] - 1) * 9
    base_query += f"&start={page_number}&rows=9"

    start = time.time()
    result = requests.get(base_query)
    end = time.time()
    time_taken = {"time_taken": end - start}
    text_dict = {"text": text}
    facet_dict = {"facet": facet}
    result = result.json()
    result.update(time_taken)
    result.update(text_dict)
    result.update(facet_dict)
    return result


@app.route('/mlt_query', methods=["POST"])
def mlt_query():
    data_list = request.get_json()
    facet_fields = {
        "size": data_list["size"],
    }

    # Declare Variables
    format_service = ""
    format_product = ""
    format_color = ""
    format_sentiment = ""

    if data_list["service_provider"]:
        format_service = "%22" + quote(data_list["service_provider"]) + "%22"

    if data_list["product_grade"]:
        format_product = "%22" + quote(data_list["product_grade"]) + "%22"

    if data_list["color"]:
        format_color = "%22" + quote(data_list["color"]) + "%22"

    if data_list["sentiment"]:
        format_sentiment = data_list["sentiment"]
        if format_sentiment != 1:
            format_sentiment = quote(format_sentiment)

    facet_fields["service_provider"] = format_service
    facet_fields["product_grade"] = format_product
    facet_fields["color"] = format_color
    facet_fields["sentiment"] = format_sentiment

    base_mlt = "http://localhost:8983/solr/amazon_iphone/mlt?"

    if data_list["search_term"]:
        format_search_term = quote(data_list['search_term'])
        base_mlt += "q=reviewDescription:" + '%22' + f"{format_search_term}" + '%22'

    base_mlt += "&fl=*"
    base_mlt += "&mlt.fl=reviewDescription&"

    count = 0
    for field, value in facet_fields.items():
        if value and count == 0:
            base_mlt += f"&fq={field}:{value} AND "
            count += 1
        elif value:
            base_mlt += f"{field}:{value} AND "

    base_mlt = base_mlt.rstrip(' AND ')

    if count == 1:
        base_mlt += "&"

    text = ""
    facet = ""
    headers = {"Content-Type": "application/json"}
    if data_list["page"] == 1:
        # Facet and Text Counting for Data Analysis
        additional_params = "rows=500&facet=true"
        for field, value in facet_fields.items():
            additional_params += f"&facet.field={field}"
        result = requests.get(base_mlt + additional_params, headers=headers).json()
        if len(result['response']['docs']) != 0:
            for i in result['response']['docs']:
                text = text + "," + i['reviewDescription']

            if result['facet_counts']['facet_fields']:
                facet = json.dumps(result['facet_counts']['facet_fields'])

    page_number = (data_list["page"] - 1) * 9
    base_mlt += f"&start={page_number}&rows=9"

    start = time.time()
    result = requests.get(base_mlt, headers=headers)
    end = time.time()
    time_taken = {"time_taken": end - start}
    text_dict = {"text": text}
    facet_dict = {"facet": facet}
    result = result.json()
    result.update(time_taken)
    result.update(text_dict)
    result.update(facet_dict)
    return result


if __name__ == '__main__':
    app.run()
