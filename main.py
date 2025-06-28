# AIcess : NeuroBudget
# Flask + Bootstrap Starter for FinFriendly (Mobile-Styled Web App)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime

app = Flask(__name__)

# ---- Mock Data ----
user_data = {
    "income": 3000,
    "expenses": {
        "food_delivery": 350,
        "groceries": 400,
        "subscriptions": 120,
    },
    "reminders": [
        {"title": "Weekly Spending Review", "day": "Sunday", "time": "20:00", "urgency": "low"},
        {"title": "Pay Internet Bill", "day": "Monday", "time": "10:00", "urgency": "high"}
    ],
    "guardrails": {
        "food_delivery_limit": 200,  # weekly
        "spending_freeze_hours": (20, 8)  # 8PM to 8AM
    }
}

# ---- Routes ----
@app.route("/")
def home():
    today = datetime.datetime.now().strftime("%A")
    return render_template("dashboard.html", reminders=user_data["reminders"], today=today)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")
    # Simulate AI response (replace with OpenAI later)
    response = "If you're spending $350 on food delivery, try limiting it to $200 weekly and cook 2 more meals."
    return jsonify({"reply": response})

@app.route("/guardrails")
def guardrails():
    food_delivery = user_data["expenses"]["food_delivery"]
    limit = user_data["guardrails"]["food_delivery_limit"]
    over_limit = food_delivery > limit
    return jsonify({"status": "over" if over_limit else "ok", "current": food_delivery, "limit": limit})

# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True)
