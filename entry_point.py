from simplexml import dumps, element_from_dict
from dicttoxml import dicttoxml
from flask import Flask, request, jsonify, g, Response, make_response
from src.estimator import estimator
import time

app = Flask(__name__)


@app.before_request
def before_req():
    g.start = time.time() * 1000


@app.after_request
def after_req(response):
    f = open('log.txt', 'a+')
    req_method = request.method
    req_path = request.path
    res_time = round(time.time() * 1000 - g.start)
    res_status_code = response.status_code

    f.write("{} \t\t {} \t\t {} \t\t {} ms \n".format(req_method, req_path, res_status_code, res_time))
    f.close()
    return response


@app.route('/')
def home():
    return "Hello, Word"


@app.route('/api/v1/on-covid-19', methods=['POST'])
def get_estimation_default():
    req_data = request.get_json()
    res = estimator(req_data)
    return jsonify(res)


@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def get_estimation_json():
    return get_estimation_default()


@app.route('/api/v1/on-covid-19/xml', methods=['POST', 'GET'])
def get_estimation_xml():
    req_data = request.get_json()

    res = dicttoxml(estimator(req_data), attr_type=False)
    # res = estimator(req_data)
    # res = dumps({'root': estimator(req_data)})

    r = make_response(res)
    r.headers["Content-Type"] = "application/xml; charset=utf-8"
    return r


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def get_logs():
    f = open('log.txt', 'r')
    contents = f.read()
    f.close()
    return contents


if __name__ == '__main__':
    app.run(debug=True)
