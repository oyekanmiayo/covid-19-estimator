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
    res_time = int(time.time() * 1000 - g.start)
    res_status_code = response.status_code

    f.write("{}\t{}\t{}\t0{}ms\n".format(req_method, req_path, res_status_code, res_time))
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
    if request.method == 'POST':
        req_data = request.get_json()

        res = dicttoxml(estimator(req_data), attr_type=False)
        # res = estimator(req_data)
        # res = dumps({'root': estimator(req_data)})
    else:
        res_dict = {'message': 'Run POST passing data to receive estimate in xml.'}
        res = dicttoxml(res_dict, attr_type=False)

    r = make_response(res)
    r.headers["Content-Type"] = "application/xml; charset=utf-8"
    return r


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def get_logs():
    f = open('log.txt', 'r')
    contents = f.read()
    f.close()
    r = make_response(contents)
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return contents


if __name__ == '__main__':
    app.run(debug=True)
