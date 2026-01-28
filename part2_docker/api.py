from flask import Flask
from flask import request, jsonify
from part2_docker.model_utils import predict #type: ignore
import time

app = Flask(__name__)

app_start_time = time.time()
requests_count = 0
response_time_list = []

@app.route("/", methods=["GET"])
def index():
    return "Churn Prediction API - Available Endpoints: /health [GET], /metrics [GET], /api/predict [POST]", 200

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/api/predict", methods=["POST"])
def predict_label():
    global requests_count, response_time_list
    start_time = time.time()

    data = request.get_json()
    if isinstance(data, dict):
        data = [data]

    predictions, probabilities = predict(data)

    response_time = time.time() - start_time
    requests_count += 1
    response_time_list.append(response_time)

    response = {"predictions": predictions, "probabilities": probabilities}
    return jsonify(response), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    uptime = int(time.time() - app_start_time)
    avg_ms = (sum(response_time_list) / requests_count * 1000) if requests_count else 0
    metrics_data = {
        "requests_count": requests_count,
        "last_response_time_ms": response_time_list[-1] * 1000 if response_time_list else 0,
        "average_response_ms": avg_ms,
        "server_uptime_seconds": uptime,
    }
    return jsonify(metrics_data), 200