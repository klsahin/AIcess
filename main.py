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
        "food_delivery_limit": 200,
        "groceries_limit": 300,
        "subscriptions_limit": 100,
        "spending_freeze_hours": (20, 8)
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
    evaluations = {}
    for category, value in user_data["expenses"].items():
        limit_key = f"{category}_limit"
        if limit_key in user_data["guardrails"]:
            limit = user_data["guardrails"][limit_key]
            evaluations[category] = {
                "current": value,
                "limit": limit,
                "status": "over" if value > limit else "ok"
            }
    return jsonify(evaluations)

@app.route("/set-guardrails", methods=["GET", "POST"])
def set_guardrails():
    if request.method == "POST":
        data = request.form
        for key in user_data["guardrails"]:
            if key != "spending_freeze_hours" and key in data:
                user_data["guardrails"][key] = int(data.get(key))
        user_data["guardrails"]["spending_freeze_hours"] = (
            int(data.get("freeze_start", 20)),
            int(data.get("freeze_end", 8))
        )
        return redirect(url_for("home"))
    return render_template("set_guardrails.html", guardrails=user_data["guardrails"])

# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True)