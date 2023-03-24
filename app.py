from flask import Flask
import requests

app = Flask(__name__)

SORL_URL = "http://localhost:8983/solr/test/select?indent=true&q.op=OR&q=ratingScore%3A%204.0&rows=100"


@app.route('/query1')
def query1():
    params = {
        'rows': 10,
        'start': 0,
        'wt': 'json'
    }
    response = requests.get(SORL_URL, params=params)
    response_data = response.json()
    return response_data


if __name__ == '__main__':
    app.run()
