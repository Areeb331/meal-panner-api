import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def call_together_gpt(prompt):
    if not TOGETHER_API_KEY:
        return "\u274c TOGETHER_API_KEY not set"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("\u274c GPT API Error:", str(e))
        return "\u26a0\ufe0f GPT could not generate a meal plan. Please try again."
