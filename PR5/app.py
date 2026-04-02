from flask import Flask, render_template, jsonify, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

app = Flask(__name__)

# Завантажуємо датасет (має колонку yield)
df = pd.read_csv("Crop_recommendation_with_yield.csv")

X_class = df.drop(["label", "yield"], axis=1)
y_class = df["label"]

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42
)

model_class = RandomForestClassifier(n_estimators=100, random_state=42)
model_class.fit(X_train_c, y_train_c)

X_reg = df.drop(["label", "yield"], axis=1)  # тільки числові ознаки
y_reg = df["yield"]

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

model_reg = RandomForestRegressor(n_estimators=100, random_state=42)
model_reg.fit(X_train_r, y_train_r)

@app.route("/")
def index():
    crops = df["label"].unique().tolist()
    return render_template("index.html", crops=crops)

@app.route("/data")
def get_data():
    crop = request.args.get("crop")
    if crop and crop != "all":
        data = df[df["label"] == crop].to_dict(orient="records")
    else:
        data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/predict", methods=["POST"])
def predict():
    values = request.json
    input_df = pd.DataFrame([values])

    # Передбачення культури
    prediction_crop = model_class.predict(input_df)[0]

    # Передбачення врожайності
    prediction_yield = model_reg.predict(input_df)[0]

    return jsonify({
        "prediction_crop": prediction_crop,
        "prediction_yield": round(prediction_yield, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
