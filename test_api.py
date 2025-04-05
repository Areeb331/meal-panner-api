import requests

url = "https://meal-panner-api-production-e2b2.up.railway.app/generate-meal-plan"

data = {
  "uid": "test123",
  "age": 23,
  "gender": "Male",
  "bmi": 21.4,
  "goal": "Weight Gain",
  "activity_level": "Moderate",
  "weight_kg": 60,
  "desired_weight": 70,
  "protein_sources": ["Eggs", "Chicken"],
  "carb_sources": ["Rice", "Bread"],
  "fat_sources": ["Nuts", "Olive oil"],
  "fruits": ["Banana", "Apple"],
  "vegetables": ["Spinach", "Carrots"],
  "seafood": ["None"],
  "beverages": ["Smoothies", "Milk"],
  "sweet_frequency": "Occasionally",
  "cooking_time": "Less than 30 minutes",
  "preferred_cooking_style": ["Boiled", "Grilled"],
  "hot_or_cold_meals": "Mostly hot meals",
  "food_dislikes": ["Spicy", "Oily"],
  "workout_type": "Weight training",
  "workout_frequency": "3-4 days/week",
  "calories_goal": 2800,
  "protein_goal": 160,
  "carbs_goal": 350,
  "fats_goal": 90
}


response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:")
try:
    print(response.json())
except Exception as e:
    print("Raw Response:", response.text)
