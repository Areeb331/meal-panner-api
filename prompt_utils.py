import re
def build_dynamic_prompt(user_data, day_range="1-7"):
    # 🔄 Normalize keys
    key_mapping = {
        "protein_sources": "protein_choices",
        "carb_sources": "carb_choices",
        "fat_sources": "fats_choices",
        "fruits": "fruit_choices",
        "vegetables": "vegetable_choices",
        "beverages": "beverage_preference",
        "preferred_cooking_style": "cooking_styles",
        "sweet_frequency": "dessert_frequency"
    }
    for old, new in key_mapping.items():
        if old in user_data:
            user_data[new] = user_data.pop(old)

    # ✅ Basic info
    goal = user_data.get("goal", "Not specified").title()
    age = user_data.get("age", "Not specified")
    gender = user_data.get("gender", "Not specified")
    bmi = user_data.get("bmi", "Not specified")

    # 🏋️‍♂️ Workout
    workout_instruction = ""
    if user_data.get("workout_type") or user_data.get("workout_frequency"):
        workout_instruction = f"- Include one short workout suggestion per day: {user_data.get('workout_type', '')} ({user_data.get('workout_frequency', '')})"

    # 🍽️ Preferences
    preferences = []

    def add_pref(key):
        val = user_data.get(key)
        if isinstance(val, list) and val:
            preferences.append(f"{key.replace('_', ' ').title()}: {', '.join(val)}")
        elif isinstance(val, str) and val.strip():
            preferences.append(f"{key.replace('_', ' ').title()}: {val}")

    keys = [
        "weight_gain_goal", "weight_gain_amount", "weight_loss_goal", "eating_schedule", "activity_level",
        "protein_choices", "carb_choices", "vegetable_choices", "fruit_choices", "grain_choices",
        "fats_choices", "seafood_choices", "cooking_styles", "pasta_rice_choices", "pulse_choices",
        "snack_choices", "beverage_preference", "dessert_frequency", "sweet_choices", "salty_snacks",
        "spices_choices", "cooking_time", "allergies", "hot_or_cold_meals", "food_dislikes"
    ]
    for k in keys:
        add_pref(k)

    pref_text = "\n".join(f"- {p}" for p in preferences)

    return f"""
You are a certified AI dietitian. Create a **strictly structured 7-day meal plan** for Days {day_range}. Follow these rules exactly:

User Info:
- Goal: {goal}
- Age: {age}, Gender: {gender}, BMI: {bmi}
- Preferences:
{pref_text}

Meal Plan Rules:
- Provide exactly 7 full days of meals. Each day MUST start with "Day X:"
- Each day must contain exactly 3 meals: Breakfast, Lunch, Dinner
- Don't show any meals except these 3: Breakfast, Lunch, Dinner
- Each meal must include nutritional info:
  - Calories (kcal), Protein (g), Carbs (g), Fats (g)
- End each day with: 
  Total Daily Nutrition: Calories: ___ kcal, Protein: ___g, Carbs: ___g, Fats: ___g
- DO NOT include:
  - Any recipes, cooking steps, ingredients list, or preparation tips
  - Disclaimers or statements like “consult a dietitian”
  - BMR, TDEE, macros calculations
  - “Here’s your meal plan” style intro
  - Anything outside Day {day_range.split("-")[0]} to Day {day_range.split("-")[1]}
  - Make sure each meal shows its nutrition like:
    Calories: 550 kcal, Protein: 45g, Carbs: 55g, Fats: 12g
    Do not change this format. Always use this exact structure after each meal.
- If the user wants to gain weight, provide high-calorie food options.
- If the user wants to lose weight, provide low-calorie food options.


Additional Instructions:
{workout_instruction}
- Respect food dislikes and allergies completely.
- Keep each day's content concise and strictly formatted.

Start directly like this:
Day {day_range.split("-")[0]}:
Breakfast: ...
Calories: ..., Protein: ..., Carbs: ..., Fats: ...
""".strip()


def clean_response(text):
    text = text.replace("**", "").replace("###", "")
    text = re.sub(r"(?i)^here.*?plan:?\n?", "", text)
    return text.strip()
