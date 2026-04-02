from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

FIREBASE_URL = "https://smartsocket-6306a-default-rtdb.europe-west1.firebasedatabase.app/logs.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    # робимо запит до Firebase
    response = requests.get(FIREBASE_URL)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Не вдалося отримати дані з Firebase"})
    
if __name__ == "__main__":
    app.run(debug=True)
