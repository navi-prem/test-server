import json
from flask import Flask, request
from flask_cors import CORS
from gradio_client import Client
from math import ceil
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

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

            doctor["viable"] = result
            crowd = pd.DataFrame(doctor["crowd"])
            model = ARIMA(crowd, order=(5, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)
            doctor["estimate"] = str(ceil(forecast.values[0]))

            o.append(doctor)

        return json.dumps(o)
