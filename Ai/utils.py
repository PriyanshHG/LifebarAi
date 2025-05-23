import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    """Check if uploaded file is image"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_response(food_name, calories, impact_minutes):
    """Format the final response to send to frontend"""
    impact_text = f"+{impact_minutes} mins" if impact_minutes > 0 else f"{impact_minutes} mins"
    return {
        "food": food_name,
        "calories": int(calories),
        "impact": impact_minutes,
        "impact_text": impact_text,
        "status": "success"
    }

def log_food_analysis(food_name, calories, impact_minutes):
    """Log analysis result for debugging or analytics"""
    logging.info(f"Analyzed: {food_name} | Calories: {calories} | Impact: {impact_minutes} mins")

def get_food_from_csv(food_item, food_data):
    """Match food from CSV and return calories & impact"""
    result = food_data[food_data["food_item"] == food_item.lower()]
    if result.empty:
        return None
    return {
        "calories": result["calories"].values[0],
        "impact": result["life_minutes_impact"].values[0]
    }
