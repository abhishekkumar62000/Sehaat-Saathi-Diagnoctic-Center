import random
import os
from openai import OpenAI
from decouple import config

# Retrieve API key from environment variables using decouple for .env file support
# Fallback to os.getenv properly in case decouple fails or for standard usage
try:
    OPENAI_API_KEY = config('OPENAI_API_KEY', default=None)
except:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_health_advice(user_input, context, chat_history=None):
    """
    Generates health advice using OpenAI 'gpt-4o-mini' as an AI Doctor.
    
    Args:
        user_input (str): The user's question.
        context (dict): Dictionary containing prediction details (disease, result, related_data).
        chat_history (list): List of previous messages [{"role": "user", "content": "..."}, ...]
        
    Returns:
        str: The chatbot's response.
    """
    if chat_history is None:
        chat_history = []
        
    # ------------------------------------------------------------------
    # IMPLEMENTATION OPTION 1: REAL LLM (OpenAI) - PRIMARY
    # ------------------------------------------------------------------
    if OPENAI_API_KEY:
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            # Construct the system persona
            system_prompt = f"""
            You are Dr. AI, a senior virtual medical consultant and Health Guardian.
            
            YOUR MISSION:
            1. Provide accurate, empathetic, and professional medical guidance.
            2. Act as a 'One-to-One' private personal doctor for the user.
            3. CRITICAL: If the user inputs symptoms of a medical EMERGENCY (e.g., chest pain, severe bleeding, difficulty breathing, stroke signs, suicide ideation), start your response with: "PLEASE CALL EMERGENCY SERVICES IMMEDIATELY." Then provide temporary first-aid advice.
            4. Keep answers concise (under 150 words) unless complex explanation is asked.
            5. Use the provided DIAGNOSTIC CONTEXT to tailor your answer if relevant.
            
            DIAGNOSTIC CONTEXT (Current User Status):
            - Condition Checked: {context.get('disease', 'General Checkup')}
            - Prediction Result: {context.get('result', 'Not specified')}
            - Clinical Data: {context.get('data', 'None')}
            
            TONE:
            - Professional but warm.
            - Authoritative but safe (always recommend a real doctor for final diagnosis).
            - Use clear formatting (bullet points) for treatments/suggestions.
            """
            
            # Build the message chain
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add limited history (last 4-5 messages) to maintain context without token overflow
            # Filter out any system messages from history if they exist, just take user/assistant
            for msg in chat_history[-5:]: 
                messages.append({"role": msg["role"], "content": msg["content"]})
                
            # Add current query
            messages.append({"role": "user", "content": user_input})
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.4, # Slightly creative but focused
                max_tokens=350,  # Allow enough room for thorough medical advice
                presence_penalty=0.6 # Encourage new information, less repetition
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            # Fallback to local logic if server fails
            pass
    
    # ------------------------------------------------------------------
    # IMPLEMENTATION OPTION 2: FALLBACK (Simulated)
    # ------------------------------------------------------------------
    return local_fallback_response(user_input, context)

def local_fallback_response(user_input, context):
    """Original Rule-based logic moved here as backup"""
    disease = context.get('disease', 'General Health')
    result = context.get('result', 'Unknown')
    user_input_lower = user_input.lower()
    
    if "emergency" in user_input_lower or "pain" in user_input_lower:
         return "If this is a medical emergency, please call your local emergency number immediately. For non-emergencies, I recommend seeing a specialist."

    if "doctor" in user_input_lower or "appointment" in user_input_lower:
        return "I strongly recommend scheduling an appointment with a specialist to discuss these results further."

    if disease == "Diabetes" and ("High" in str(result) or str(result) == "1"):
        if "diet" in user_input_lower:
            return "Focus on a low-glycemic diet. Avoid sugary drinks and processed snacks. Eat leafy greens and whole grains."
        return "With potential diabetes signs, monitoring blood sugar is key. Consult a doctor for a plan."

    elif disease == "Heart Disease" and ("High" in str(result) or str(result) == "1"):
        if "diet" in user_input_lower:
            return "Reduce salt (sodium) and saturated fats. Eat more fruits, veggies, and oily fish."
        return "Heart health is vital. Please consult a cardiologist immediately."

    return f"Based on your checkup for {disease}, maintaining a healthy lifestyle is key. Please consult a doctor for a specific treatment plan."
