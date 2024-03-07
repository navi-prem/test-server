from flask import Flask, request
from flask_cors import CORS
from gradio_client import Client

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/cimta", methods=["POST"])
def cimta():
    if request.method == "POST":
        pending_patients_count, avg_wait_time, time, rating = (
            request.json["pending_patients_count"],
            request.json["avg_wait_time"],
            request.json["time"],
            request.json["rating"],
        )
        client = Client("aswatht/cimta")
        result = client.predict(
            pending_patients_count,
            avg_wait_time,
            time,
            rating,
            api_name="/predict",
        )
        return result
