from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
USDA_API_KEY = "YOUR_USDA_API_KEY"

@app.route("/analyze", methods=["POST"])
def analyze_food():
    data = request.get_json()
    food_name = data.get("food")

    # Step 1: USDA API se nutrition data lena
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query= {food_name}&pageSize=1&api_key={USDA_API_KEY}"
    response = requests.get(url)
    result = response.json()

    if not result.get("foods"):
        return jsonify({"error": "Food not found"}), 404

    nutrients = result["foods"][0]["foodNutrients"]
    calories = next((n for n in nutrients if n["nutrientId"] == 1008), {}).get("value", 0)

    # Step 2: Lifespan impact calculate karna
    protein = next((n for n in nutrients if n["nutrientId"] == 1003), {}).get("value", 0)
    fat = next((n for n in nutrients if n["nutrientId"] == 1004), {}).get("value", 0)
    sugar = next((n for n in nutrients if n["nutrientName"] == "Sugars, total including NME"), {}).get("value", 0)

    lifespanImpact = round(
        (calories * 0.1) -
        (fat * 0.5 * 60) -
        (sugar * 0.2 * 60) +
        (protein * 0.3 * 60)
    )

    return jsonify({
        "food": food_name,
        "calories": calories,
        "impact": lifespanImpact
    })

if __name__ == "__main__":
    app.run(debug=True)
