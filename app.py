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


@app.route('/general_query', methods=["POST"])
def general_query():
    data_list = request.get_json()
    facet_fields = {
        "size": data_list["size"],
        "critic": data_list["critic"]
    }
    # Declare Variables
    format_service = ""
    format_product = ""
    format_color = ""

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

    # Adding it to the facet fields dictionary
    facet_fields["service_provider"] = format_service
    facet_fields["product_grade"] = format_product
    facet_fields["color"] = format_color

    base_query = "http://localhost:8983/solr/amazon_iphone/select?defType=dismax&q="
    if data_list["search_term"]:
        format_search_term = quote(data_list["search_term"])
        base_query += format_search_term + "&mm=1&"
        # Assigning importance to reviewDescription
        base_query += "qf=reviewDescription&"
    else:
        base_query += "*:*&"

    count = 0
    for field, value in facet_fields.items():
        if value and count == 0:
            base_query += f"fq={field}:{value} AND "
            count += 1
        elif value:
            base_query += f"{field}:{value} AND "

    base_query = base_query.rstrip(' AND ')

    # Adding Page Numbers
    page_number = (data_list["page"] - 1) * 9
    base_query += f"&start={page_number}&rows=9"

    headers = {"Content-Type": "application/json"}
    start = time.time()
    result = requests.get(base_query, headers=headers)
    end = time.time()
    time_taken = {"time_taken": end - start}
    result = result.json()
    result.update(time_taken)
    return result

# facet_q = "facet.field"
    #
    # if any(facet_fields.values()):
    #     base_query += "facet=true&"
    #
    # for field, value in facet_fields.items():
    #     if value:
    #         base_query += f"{facet_q}={field}&"
    #
    # for field, value in facet_fields.items():
    #     if value:
    #         base_query += f"fq={field}:{value} AND "
    #


@app.route('/mlt_query', methods=["POST"])
def mlt_query():
    data_list = request.get_json()
    facet_fields = {
        "size": data_list["size"],
        "color": data_list["color"],
        "critic": data_list["critic"],
    }
    if len(data_list["service_provider"]) > 1:
        format_service = "%22" + quote(data_list["service_provider"]) + "%22"
        facet_fields["service_provider"] = format_service
    else:
        facet_fields["service_provider"] = data_list["service_provider"]

    if len(data_list["product_grade"]) > 1:
        format_product = "%22" + quote(data_list["product_grade"]) + "%22"
        facet_fields["product_grade"] = format_product
    else:
        facet_fields["product_grade"] = data_list["product_grade"]

    base_mlt = "http://localhost:8983/solr/amazon_iphone/mlt?"

    if data_list["search_term"]:
        base_mlt += f"mlt.q=reviewDescription:{data_list['search_term']}"

    base_mlt += "&fl=*"
    base_mlt += "&mlt.fl=reviewDescription&"

    page_number = (data_list["page"] - 1) * 9
    base_mlt += f"start={page_number}&rows=9"

    if any(facet_fields.values()):
        base_mlt += "&facet=true&"

    facet_q = "facet.field"

    for field, value in facet_fields.items():
        if value:
            base_mlt += f"{facet_q}={field}&fq={field}:{value}&"

    base_mlt = base_mlt.rstrip('&')
    query_result = {"base_mlt": base_mlt}
    return query_result

    # headers = {"Content-Type": "application/json"}
    # start = time.time()
    # result = requests.get(base_mlt, headers=headers)
    # end = time.time()
    # time_taken = {"time_taken": end - start}
    # result = result.json()
    # result.update(time_taken)
    # return result


if __name__ == '__main__':
    app.run()
