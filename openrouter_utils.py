import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # You can change this to gpt-4 if you upgrade
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800  # ✅ Important: Shorten to avoid free quota errors
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response_json = response.json()

        # ✅ Handle quota or token limit errors
        if "error" in response_json:
            print("❌ GPT API error:", response_json["error"])
            return "⚠️ GPT could not generate a meal plan. Please try again."

        # ✅ Return content if available
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            print("⚠️ GPT returned no choices:", response_json)
            return "⚠️ GPT could not generate a meal plan. Please try again."

    except Exception as e:
        print("❌ Request Failed:", e)
        return "❌ GPT API failed. Please try again later."
