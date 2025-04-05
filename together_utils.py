import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def call_together_gpt(prompt):
    if not TOGETHER_API_KEY:
        return "❌ TOGETHER_API_KEY not set"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # ✅ Model name is correct
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        print("❌ Timeout: GPT took too long.")
        return "⚠️ GPT request timed out. Please try again later."
    except Exception as e:
        print("❌ GPT API Error:", str(e))
        return "⚠️ GPT could not generate a meal plan. Please try again."
