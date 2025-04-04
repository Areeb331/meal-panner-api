from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from prompt_utils import build_dynamic_prompt
from openrouter_utils import call_openrouter_gpt
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # ✅ Enables Android + web access

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

        if "Invalid:" in full_plan or "sample" in full_plan.lower():
            return jsonify({'meal_plan': "⚠️ GPT could not generate a meal plan. Please try again."}), 400

        return jsonify({'meal_plan': full_plan})

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
