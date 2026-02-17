def get_roadmap_data(goal, diet_type):
    # Simplified logic for demonstration. In a real app, this would be more complex.
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = []

    # --- BASE TEMPLATES ---
    veg_meals = {
        'breakfast': ["Oatmeal with fruits", "Greek yogurt with honey", "Whole grain toast with avocado", "Poha with veggies", "Vegetable smoothie"],
        'lunch': ["Lentil soup with brown rice", "Quinoa salad with chickpeas", "Paneer stir-fry with roti", "Mixed vegetable curry", "Dal Tadka with salads"],
        'dinner': ["Grilled veggies with tofu", "Spinach soup with toast", "Khichdi", "Salad bowl", "Steamed momos (veg)"],
        'snack': ["Almonds & Walnuts", "Apple", "Carrot sticks", "Green tea", "Roasted Chana"]
    }

    non_veg_meals = {
        'breakfast': ["Boiled eggs with toast", "Chicken sausage with bagel", "Omelette with spinach", "Chicken sandwich", "Protein smoothie"],
        'lunch': ["Grilled chicken with salad", "Fish curry with rice", "Chicken stir-fry", "Egg curry with roti", "Tuna salad"],
        'dinner': ["Baked salmon", "Chicken soup", "Grilled turkey", "Lean beef stir-fry", "Egg salad"],
        'snack': ["Boiled egg", "Protein bar", "Greek yogurt", "Jerky", "Nuts"]
    }
    
    meals = veg_meals if diet_type == 'Vegetarian' or diet_type == 'Vegan' else non_veg_meals # Simplify for now
    
    # --- GOAL ADJUSTMENTS ---
    exercise_plan = "30 mins walking"
    tips = "Stay hydrated."

    if goal == 'Weight Loss':
        exercise_plan = "45 mins cardio + HIIT"
        tips = "Create a calorie deficit. Avoid sugar completely."
    elif goal == 'Muscle Gain':
        exercise_plan = "60 mins weight lifting (Hypertrophy)"
        tips = "Focus on high protein intake. Eat post-workout."
    elif goal == 'Diabetes Management':
        exercise_plan = "30 mins brisk walking after meals"
        tips = "Monitor blood sugar. Eat low GI foods."
        # Override sugary items
        meals['breakfast'] = ["Steel-cut oats (unsweetened)", "Vegetable Dalia", "Moong Dal Chilla", "Boiled Eggs", "Avocado toast"]
    elif goal == 'Heart Health':
        exercise_plan = "40 mins moderate cardio (Swimming/Cycling)"
        tips = "Low sodium diet. Eat healthy fats (Nuts/Fish)."

    import random
    
    for day in days:
        day_plan = {
            'day': day,
            'breakfast': random.choice(meals['breakfast']),
            'lunch': random.choice(meals['lunch']),
            'dinner': random.choice(meals['dinner']),
            'snack': random.choice(meals['snack']),
            'exercise': exercise_plan,
            'tip': tips
        }
        plan.append(day_plan)
        
    return plan
