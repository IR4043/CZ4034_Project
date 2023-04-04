import json
import requests
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/update_index', methods=['POST'])
def update_index():
    data_lst = json.loads(request.data)['docs']
    params = {"boost": 1.0, "overwrite": "true", "commitWithin": 1000}
    url = 'http://127.0.0.1:8983/solr/new_phone/update?wt=json'
    headers = {"Content-Type": "application/json"}
    result = requests.post(url, json=data_lst, params=params, headers=headers)
    return Response(result)


if __name__ == '__main__':
    app.run(debug=True)
