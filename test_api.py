import requests

url = "https://54b178d5-2fed-48c7-8ce8-4dd58eba4050-00-3g07b08jmfbr4.sisko.replit.dev/generate-meal-plan"

data = {
    "age": 22,
    "goal": "Gain weight",
    "gender": "Female",
    "height_cm": 160,
    "weight_kg": 48,
    "bmi": 18.7,
    "meals_per_day": "5-6 small meals",
    "workout_frequency": "3-5 times a week",
    "workout_type": "Weightlifting",
    "weight_gain_goal": "Build muscle",
    "weight_gain_amount": "5-10 kg (11-22 lbs)",
    "activity_level": "Moderately active (moderate exercise 3-5 days/week)",
    "beverage_preference": "Smoothies or milkshakes",
    "dessert_frequency": "Occasionally",
    "protein_choices": ["Chicken", "Fish"],
    "carb_choices": ["Oats", "Brown rice"],
    "vegetable_choices": ["Spinach", "Carrots"],
    "fruit_choices": ["Bananas", "Mangoes"],
    "grain_choices": ["Oats", "Quinoa"],
    "seafood_choices": ["Salmon", "Shrimp"],
    "fats_choices": ["Avocado", "Olive oil"],
    "cooking_styles": ["Grilling", "Steaming"],
    "allergies": ["Dairy"]
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:")
try:
    print(response.json())
except Exception as e:
    print("Raw Response:", response.text)
