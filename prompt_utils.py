def build_dynamic_prompt(user_data, day_range="1-7"):
    goal = user_data.get("goal", "").lower()
    age = user_data.get("age")
    gender = user_data.get("gender")
    bmi = user_data.get("bmi")

    # Include workout if any field is selected
    workout_instruction = ""
    if user_data.get("workout_type") or user_data.get("workout_frequency"):
        workout_instruction = f"- Add daily workout suggestions based on user preference: {user_data.get('workout_type', 'Not specified')} ({user_data.get('workout_frequency', 'Not specified')})"

    preferences = []
    def add_pref(key):
        val = user_data.get(key)
        if isinstance(val, list) and val:
            preferences.append(f"{key.replace('_', ' ').title()}: {', '.join(val)}")
        elif isinstance(val, str) and val.strip():
            preferences.append(f"{key.replace('_', ' ').title()}: {val}")

    for k in [
        "weight_gain_goal", "weight_gain_amount", "weight_loss_goal", "eating_schedule", "activity_level",
        "protein_choices", "carb_choices", "vegetable_choices", "fruit_choices", "grain_choices",
        "fats_choices", "seafood_choices", "cooking_styles", "pasta_rice_choices", "pulse_choices",
        "snack_choices", "beverage_preference", "dessert_frequency", "sweet_choices", "salty_snacks",
        "spices_choices", "cooking_time", "allergies", "hot_or_cold_meals", "food_dislikes"
    ]:
        add_pref(k)

    return f"""
You are a certified AI dietitian. Create a clean, personalized 7-day meal plan for Days {day_range}. Follow these rules strictly:

User Info:
Goal: {goal}, Age: {age}, Gender: {gender}, BMI: {bmi}
Meal Structure: Breakfast, Lunch, Dinner
{', '.join(preferences)}

Instructions:
- Show exactly 3 meals per day: Breakfast, Lunch, Dinner.
- Each meal must include: Calories (kcal), Protein (g), Carbs (g), Fats (g).
- End each day with:
  Total Daily Nutrition: Calories: ___ kcal, Protein: ___g, Carbs: ___g, Fats: ___g
{workout_instruction}
- If beverage preferences are given, include them in meals or as drinks.
- Do not include disclaimers, BMR, TDEE, or generic suggestions like "consult a dietitian".
- DO NOT say: “This is a sample plan” or add notes at the end.
- Return full details for Days {day_range}. Do NOT leave any day or meal incomplete.
- Ensure all ingredients respect allergies and dislikes.
- Include workout suggestions if given.
Start with:
Day {day_range.split('-')[0]}:
Breakfast: ...
Calories: ..., Protein: ..., Carbs: ..., Fats: ...
""".strip()
