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
        "model": "gpt-3.5-turbo",  # Change to "gpt-4" if needed and supported
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800  # Short limit to avoid quota/token issues
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response_json = response.json()

        # ✅ Handle error from OpenRouter
        if "error" in response_json:
            print("❌ GPT API error:", response_json["error"])
            return "⚠️ GPT could not generate a meal plan. Please try again."

        # ✅ Success case
        if "choices" in response_json and response_json["choices"]:
            content = response_json["choices"][0]["message"]["content"]
            print("🤖 GPT Response Content:\n", content)
            return content
        else:
            print("⚠️ GPT returned no valid choices:", response_json)
            return "⚠️ GPT could not generate a meal plan. Please try again."

    except Exception as e:
        print("❌ Request Failed:", str(e))
        return "❌ GPT API failed. Please try again later."
