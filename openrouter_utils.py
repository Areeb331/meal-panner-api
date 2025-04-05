import os
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
print("🔑 OpenRouter API Key:", OPENROUTER_API_KEY)

def call_openrouter_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 700  # ✅ Reduced to avoid OpenRouter free limit error
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response_json = response.json()

        # Debug logs
        print("📨 Sent Prompt:\n", prompt)
        print("📩 GPT Raw Response:\n", response_json)

        if "error" in response_json:
            print("❌ GPT API error:", response_json["error"])
            return "⚠️ GPT could not generate a meal plan. Please try again."

        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]

        return "⚠️ GPT could not generate a meal plan. Please try again."

    except Exception as e:
        print("❌ Request Failed:", e)
        return "❌ GPT API failed. Please try again later."
