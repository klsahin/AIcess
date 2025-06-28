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
    user_input = request.json.get("message", "").strip().lower()
    if "spending limit" in user_input:
        response = "Your weekly spending limits are: Food Delivery $200, Groceries $300, Subscriptions $100."
    elif "save more" in user_input:
        response = "Try meal prepping and canceling unused subscriptions to save more each month!"
    elif "current spending" in user_input:
        response = "This week, you've spent $350 on food delivery, $400 on groceries, and $120 on subscriptions."
    else:
        response = "I'm here to help! Ask me about your spending, limits, or saving tips."
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

@app.route("/notifications")
def notifications():
    notifications = [
        {"title": "Payment Reminder", "message": "Your credit card bill is due tomorrow.", "time": "09:00 AM"},
        {"title": "Recurring Routine", "message": "Weekly Spending Review every Saturday @ 8PM", "time": "08:00 PM"},
        {"title": "Impulse Guard Triggered", "message": "Spending on subscriptions exceeded your limit.", "time": "11:30 AM"}
    ]
    return render_template("notifications.html", notifications=notifications)

@app.route("/chat-popup")
def chat_popup():
    return render_template("chat_popup.html")

@app.route("/weekly-review")
def weekly_review():
    return render_template("weekly_review.html")

@app.route("/guardrail-insights")
def guardrail_insights():
    return render_template("guardrail_insights.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True)
