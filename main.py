from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from prompt_utils import build_dynamic_prompt
from openrouter_utils import call_openrouter_gpt
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_service_key.json")  # 🔑 Your service account key file
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def index():
    return '✅ Flask is working! Visit /generate-meal-plan to test POST requests.'

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    user_data = request.get_json()
    print("📦 Received user_data:", user_data)

    try:
        prompt_1 = build_dynamic_prompt(user_data, day_range="1-4")
        print("📨 Prompt 1:\n", prompt_1)
        response_1 = call_openrouter_gpt(prompt_1)
        print("🤖 Response 1:\n", response_1)

        prompt_2 = build_dynamic_prompt(user_data, day_range="5-7")
        print("📨 Prompt 2:\n", prompt_2)
        response_2 = call_openrouter_gpt(prompt_2)
        print("🤖 Response 2:\n", response_2)

        full_plan = f"{response_1.strip()}\n\n{response_2.strip()}"

        if not full_plan or len(full_plan) < 100:
            return jsonify({'meal_plan': "⚠️ GPT response was empty or too short. Try again."}), 400

        # 🔥 Extract nutrition goals from user_data if available
        uid = user_data.get("uid")
        goals = {
            "calories_goal": int(user_data.get("calories_goal", 2200)),
            "protein_goal": int(user_data.get("protein_goal", 120)),
            "fats_goal": int(user_data.get("fats_goal", 70)),
            "carbs_goal": int(user_data.get("carbs_goal", 300)),
            "calories": 0,  # initial value
            "protein": 0,
            "fats": 0,
            "carbs": 0
        }

        if uid:
            today = datetime.now().strftime("%Y-%m-%d")
            doc_ref = db.collection("users").document(uid).collection("daily_progress").document(today)
            doc_ref.set(goals, merge=True)
            print(f"✅ Daily goals saved for UID {uid} on {today}")

        return jsonify({'meal_plan': full_plan})

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
