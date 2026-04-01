from flask import Flask, render_template, jsonify
import time
import random

app = Flask(__name__)

logs = []
# Симуляція стану розетки
socket_state = {"isOn": False, "startTime": 0, "duration": 10}  # 10 секунд

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    if socket_state["isOn"]:
        elapsed = int(time.time() - socket_state["startTime"])
        remaining = max(socket_state["duration"] - elapsed, 0)
        if remaining == 0:
            socket_state["isOn"] = False  # автоматично вимикаємо
    else:
        remaining = 0
    return jsonify({"isOn": socket_state["isOn"], "remaining": remaining})

@app.route("/toggle")
def toggle():
    if not socket_state["isOn"]:
        socket_state["isOn"] = True
        socket_state["startTime"] = time.time()
    else:
        socket_state["isOn"] = False
    return jsonify(socket_state)

@app.route("/data")
def data():
    if socket_state["isOn"]:
        elapsed = int(time.time() - socket_state["startTime"])
        if elapsed >= socket_state["duration"]:
            socket_state["isOn"] = False
        else:
            # генеруємо випадкові дані температури/вологості
            temp = round(random.uniform(20, 80), 2)
            hum = round(random.uniform(30, 90), 2)
            logs.append({"time": elapsed, "temp": temp, "hum": hum})
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
