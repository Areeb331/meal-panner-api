import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def call_together_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
        res = response.json()

        print("🧠 Prompt Sent:", prompt)
        print("📩 GPT Response:", res)

        if "choices" in res:
            return res["choices"][0]["message"]["content"]

        return "⚠️ GPT could not generate a meal plan. Please try again."

    except Exception as e:
        print("❌ TogetherAI Error:", e)
        return "❌ GPT failed. Try again later."
