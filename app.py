from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)
USDA_API_KEY = "YOUR_USDA_API_KEY"  # Replace with your real key

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

@app.route("/analyze", methods=["POST"])
def analyze_food():
    data = request.get_json()
    food_name = data.get("food")

    if not food_name:
        return jsonify({"error": "No food name provided"}), 400

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query= {food_name}&pageSize=1&api_key={USDA_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from USDA", "details": str(e)}), 500

    if not result.get("foods"):
        return jsonify({"error": "Food not found in USDA database"}), 404

    nutrients = result["foods"][0]["foodNutrients"]

    calories = next((n for n in nutrients if n["nutrientId"] == 1008), {}).get("value", 0)
    protein = next((n for n in nutrients if n["nutrientId"] == 1003), {}).get("value", 0)
    fat = next((n for n in nutrients if n["nutrientId"] == 1004), {}).get("value", 0)
    sugar = next((n for n in nutrients if n["nutrientName"] == "Sugars, total including NME"), {}).get("value", 0)

    lifespanImpact = round(
        (calories * 0.1) -
        (fat * 0.5 * 60) -
        (sugar * 0.2 * 60) +
        (protein * 0.3 * 60)
    )

    message = ""
    if lifespanImpact > 0:
        message = f"✅ This food adds {lifespanImpact} minutes to your life!"
    else:
        message = f"⚠️ This food may reduce {abs(lifespanImpact)} minutes from your life."

    return jsonify({
        "food": food_name,
        "calories": calories,
        "impact": lifespanImpact,
        "message": message
    })

if __name__ == "__main__":
    app.run(debug=True)
