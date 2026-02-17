def get_health_plan(disease_name, prediction_result):
    """
    Returns a dictionary containing Diet, Exercise, and Lifestyle advice
    based on the disease and prediction result.
    
    prediction_result: Often 1 (Positive/Risk) or 0 (Negative/Safe), 
                       but varies by model. We assume logical 'True' means Risk.
    """
    
    # Standardize result to Boolean: True = Has Disease/Risk, False = Healthy
    is_risk = False
    if isinstance(prediction_result, (int, float, str)):
        try:
            # Adjust based on how your specific models return data
            # Assuming 1 = Risk, 0 = No Risk for most
            if int(prediction_result) == 1:
                is_risk = True
        except:
            pass
            
    # Default Plan (General Wellness)
    plan = {
        "status": "Safe",
        "title": "Maintaing Good Health",
        "diet": [
            "Maintain a balanced diet rich in fruits and vegetables.",
            "Stay hydrated: Drink at least 8 glasses of water a day.",
            "Limit processed foods and sugary drinks."
        ],
        "exercise": [
            "Aim for at least 30 minutes of moderate activity daily.",
            "Regular walking or jogging.",
            "Yoga or stretching for flexibility."
        ],
        "lifestyle": [
            "Ensure 7-9 hours of quality sleep.",
            "Manage stress through meditation or hobbies.",
            "Regular health checkups annually."
        ]
    }

    if not is_risk:
        return plan

    # --- SPECIFIC PLANS FOR RISKS ---
    
    plan["status"] = "Risk Identified"
    
    if disease_name == "Diabetes":
        plan["title"] = "Diabetes Management Plan"
        plan["diet"] = [
            "Low Glycemic Index foods: Whole grains, lentils, beans.",
            "Avoid sugar: Soda, candies, white bread, pasta.",
            "Eat fiber-rich veggies: Spinach, broccoli, green beans.",
            "Control portion sizes to manage blood sugar spikes."
        ]
        plan["exercise"] = [
            "Brisk walking for 30-45 mins daily (highly effective).",
            "Resistance training (light weights) 2-3 times a week.",
            "Cycling or swimming."
        ]
        plan["lifestyle"] = [
            "Monitor blood sugar levels regularly.",
            "Check feet daily for cuts or sores.",
            "Quit smoking if applicable.",
            "Manage stress levels as stress raises blood sugar."
        ]

    elif disease_name == "Heart Disease":
        plan["title"] = "Heart Health Recovery Plan"
        plan["diet"] = [
            "Heart-healthy fats: Olive oil, avocado, nuts (walnuts/almonds).",
            "Reduce Sodium: Limit salt intake to lower blood pressure.",
            "Fatty Fish: Salmon or mackerel (Omega-3 fatty acids).",
            "Avoid trans fats and saturated fats (fried foods)."
        ]
        plan["exercise"] = [
            "Aerobic exercise: Walking, swimming, light jogging.",
            "Aim for 150 minutes of moderate intensity per week.",
            "Avoid heavy lifting without doctor approval."
        ]
        plan["lifestyle"] = [
            "Monitor Blood Pressure daily.",
            "Weight management is crucial.",
            "Limit alcohol intake.",
            "Get enough sleep to reduce heart strain."
        ]

    elif disease_name == "Liver Disease":
        plan["title"] = "Liver Care & Recovery"
        plan["diet"] = [
            "Lean proteins: Chicken, fish, tofu (avoid red meat).",
            "Complex carbs: Oatmeal, brown rice.",
            "Coffee: Moderate black coffee consumption can be beneficial.",
            "Avoid Alcohol completely.",
            "Limit salt and sugar."
        ]
        plan["exercise"] = [
            "Aerobic exercise to reduce liver fat.",
            "Moderate intensity workouts (don't overexert).",
            "Consistency is key (30 mins daily)."
        ]
        plan["lifestyle"] = [
            "Stay hydrated to help flush toxins.",
            "Avoid self-medication (some painkillers harm the liver).",
            "Maintain a healthy weight.",
            "Vaccination for Hepatitis A and B."
        ]
        
    elif disease_name == "Breast Cancer":
        plan["title"] = "Oncology Support & Wellness"
        plan["diet"] = [
            "Plant-based focus: Fruits, vegetables, whole grains.",
            "Limit processed meat and red meat.",
            "Maintain healthy healthy weight.",
            "Green tea and cruciferous vegetables (broccoli/cauliflower)."
        ]
        plan["exercise"] = [
            "Gentle walking to combat fatigue.",
            "Yoga for flexibility and stress relief.",
            "Exercise tailored to energy levels."
        ]
        plan["lifestyle"] = [
            "Consult an Oncologist immediately for a treatment plan.",
            "Join a support group.",
            "Focus on mental health and stress reduction.",
            "Avoid smoking and alcohol."
        ]

    return plan
