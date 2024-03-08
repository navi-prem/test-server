import json
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
        o = []
        client = Client("aswatht/cimta")

        data = request.json["data"],

        for doctor in data[0]:
            result = client.predict(
                float(doctor["pending_patients_count"]),
                float(doctor["avg_wait_time"]),
                float(doctor["time"]),
                float(doctor["rating"]),
                api_name="/predict",
            )

            if result == '1':
                doctor["viable"] = True
            else:
                doctor["viable"] = False

            o.append(doctor)

        return json.dumps(o)
