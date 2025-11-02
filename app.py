from flask import Flask, render_template, request, jsonify
import random
from mealplans import mealplans

app = Flask(__name__)

def pick_meal(meals):
    return random.choice(meals)

@app.route("/")
def home():
    return render_template("chat_buttons.html")  # matches your HTML file

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_data = data.get("user_data", {})
    more = data.get("more", False)

    try:
        weight = float(user_data.get("weight", 0))
        height = float(user_data.get("height", 0)) / 100
        gender = user_data.get("gender", "male").lower()
        activity = user_data.get("activity", "medium").lower()
    except:
        return jsonify({"error": "Invalid input"}), 400

    # BMI calculation
    bmi = round(weight / (height**2), 2)
    if bmi < 18.5:
        category = "low"
        condition = "Underweight"
        advice = "Increase calorie intake with protein-rich foods."
    elif bmi <= 24.9:
        category = "normal"
        condition = "Normal"
        advice = "Maintain your diet and stay consistent."
    else:
        category = "high"
        condition = "Overweight"
        advice = "Reduce sugary and fried foods."

    # Daily calories estimation
    calories = round(weight * 30)
    if activity == "low": calories -= 200
    elif activity == "high": calories += 200
    if gender == "male": calories += 100
    else: calories -= 50

    # Pick meals
    breakfast = pick_meal(mealplans["breakfast"][category])
    lunch = pick_meal(mealplans["lunch"][category])
    dinner = pick_meal(mealplans["dinner"][category])

    if more:
        breakfast["name"] += " (Alternative)"
        lunch["name"] += " (Alternative)"
        dinner["name"] += " (Alternative)"

    plan = [breakfast, lunch, dinner]

    return jsonify({
        "bmi": bmi,
        "condition": condition,
        "advice": advice,
        "calories": calories,
        "plan": plan
    })

if __name__ == "__main__":
    app.run(debug=True)
