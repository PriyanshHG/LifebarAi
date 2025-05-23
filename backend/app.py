from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
food_data = pd.read_csv("../data/food_data.csv")

@app.route("/analyze", methods=["POST"])
def analyze():
    food_name = request.form.get("food").lower()
    result = food_data[food_data["food_item"] == food_name]

    if result.empty:
        return jsonify({"error": "Food not found!"})

    return jsonify({
        "food": food_name,
        "calories": int(result["calories"]),
        "impact": int(result["life_minutes_impact"])
    })

if __name__ == "__main__":
    app.run(debug=True)
