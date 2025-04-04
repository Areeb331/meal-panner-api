import requests

url = "https://meal-panner-api-production.up.railway.app/generate-meal-plan"

data = {
    "age": 22,
    "goal": "Gain weight",
    "gender": "Female",
    "height_cm": 160,
    "weight_kg": 48,
    "bmi": 18.7,
    "workout_type": "Weightlifting",
    "workout_frequency": "3-5 times a week",
    "weight_gain_goal": "Build muscle",
    "weight_gain_amount": "5-10 kg (11-22 lbs)",
    "activity_level": "Moderately active (moderate exercise 3-5 days/week)",
    "beverage_preference": "Smoothies or milkshakes",
    "dessert_frequency": "Occasionally",
    "protein_choices": ["Chicken", "Fish"],
    "carb_choices": ["Oats", "Brown rice"],
    "vegetable_choices": ["Spinach", "Carrots"],
    "fruit_choices": ["Banana", "Mango"],
    "grain_choices": ["Quinoa", "Whole wheat"],
    "seafood_choices": ["Tuna", "Shrimp"],
    "fats_choices": ["Avocado", "Nuts"],
    "cooking_styles": ["Boiled", "Grilled"],
    "pasta_rice_choices": ["Pasta", "Brown rice"],
    "pulse_choices": ["Lentils", "Chickpeas"],
    "snack_choices": ["Protein bars", "Fruit"],
    "spices_choices": ["Cumin", "Turmeric"],
    "sweet_choices": ["Dark chocolate"],
    "salty_snacks": ["Nuts"],
    "cooking_time": "15–30 mins",
    "allergies": [],
    "hot_or_cold_meals": "Mostly hot meals",
    "food_dislikes": ["None"]
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:")
try:
    print(response.json())
except Exception as e:
    print("Raw Response:", response.text)
