from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="climate_user",
        password="climate_pass",
        database="climate_db"
    )

@app.route("/data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM climate_logs ORDER BY created_at DESC LIMIT 50")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route("/")
def index():
    return render_template("index.html")   # повертає HTML сторінку

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
