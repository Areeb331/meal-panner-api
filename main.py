from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from prompt_utils import build_dynamic_prompt
from openrouter_utils import call_openrouter_gpt
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import re

# Load .env (for OpenRouter key etc.)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# ✅ Firebase Admin SDK Initialization from local file
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_service_key.json")  # Local JSON file
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔍 Helper to extract macros (calories, protein, etc.) from GPT response
def extract_macros(text):
    match = re.search(
        r'Total Daily Nutrition:.*?Calories:\s*(\d+)\s*kcal.*?Protein:\s*(\d+)\s*g.*?Carbs:\s*(\d+)\s*g.*?Fats:\s*(\d+)\s*g',
        text, re.IGNORECASE
    )
    if match:
        return {
            "calories": int(match.group(1)),
            "protein": int(match.group(2)),
            "carbs": int(match.group(3)),
            "fats": int(match.group(4))
        }
    return None

@app.route('/')
def index():
    return '✅ Flask is working! Visit /generate-meal-plan to test POST requests.'

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    user_data = request.get_json()
    uid = user_data.get("uid")
    today = datetime.now().strftime("%Y-%m-%d")

    if not uid:
        return jsonify({"error": "UID is missing"}), 400

    # ⛔ Check if today's meal plan already exists
    meal_ref = db.collection("users").document(uid).collection("meal_plans").document(today)
    existing = meal_ref.get()
    if existing.exists:
        print("✅ Reusing existing meal plan from Firestore")
        return jsonify({'meal_plan': existing.to_dict().get("plan", "📄 No plan found")})

    try:
        # 🧠 Generate GPT-based meal plan
        prompt_1 = build_dynamic_prompt(user_data, day_range="1-4")
        response_1 = call_openrouter_gpt(prompt_1)

        prompt_2 = build_dynamic_prompt(user_data, day_range="5-7")
        response_2 = call_openrouter_gpt(prompt_2)

        full_plan = f"{response_1.strip()}\n\n{response_2.strip()}"

        if not full_plan or len(full_plan) < 100:
            return jsonify({'meal_plan': "⚠️ GPT response was too short. Try again."}), 400

        # 📊 Extract actual macros from GPT output
        macros = extract_macros(full_plan)
        if macros is None:
            macros = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}

        # 🎯 Combine user goals + actuals
        goals = {
            "calories_goal": int(user_data.get("calories_goal", 2200)),
            "protein_goal": int(user_data.get("protein_goal", 120)),
            "carbs_goal": int(user_data.get("carbs_goal", 300)),
            "fats_goal": int(user_data.get("fats_goal", 70)),
            "calories": macros["calories"],
            "protein": macros["protein"],
            "carbs": macros["carbs"],
            "fats": macros["fats"]
        }

        # 🔥 Save both daily progress and meal plan
        db.collection("users").document(uid).collection("daily_progress").document(today).set(goals, merge=True)
        meal_ref.set({"plan": full_plan}, merge=True)

        print(f"✅ Meal Plan + Progress saved for UID: {uid} on {today}")
        return jsonify({'meal_plan': full_plan})

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
