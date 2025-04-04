from flask import Flask, request, jsonify
from dotenv import load_dotenv
from prompt_utils import build_dynamic_prompt
from openrouter_utils import call_openrouter_gpt
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask is working! Visit /generate-meal-plan to test POST requests.'

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    user_data = request.get_json()

    try:
        # --------- Build Prompt for Day 1–4 ----------
        prompt_1 = build_dynamic_prompt(user_data, day_range="1-4")
        response_1 = call_openrouter_gpt(prompt_1)

        # --------- Build Prompt for Day 5–7 ----------
        prompt_2 = build_dynamic_prompt(user_data, day_range="5-7")
        response_2 = call_openrouter_gpt(prompt_2)

        # --------- Merge Both Responses ----------
        full_plan = f"{response_1.strip()}\n\n{response_2.strip()}"

        # Optional Cleanup
        if "Invalid:" in full_plan or "sample" in full_plan.lower():
            return jsonify({'meal_plan': "Invalid: GPT returned incomplete or unwanted response."}), 400

        return jsonify({'meal_plan': full_plan})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

