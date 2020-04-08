from flask import Flask, request, jsonify
from src import estimator

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/api/v1/on-covid-19/json', methods=['POST'])
@app.route('/api/v1/on-covid-19', methods=['POST'])
def get_estimation_json():
    req_data = request.get_json()
    response = estimator.estimator(req_data)
    return jsonify(response)


@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def get_estimation_xml():
    pass
