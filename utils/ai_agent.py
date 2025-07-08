from dotenv import load_dotenv
import os
import google.generativeai as genai

#Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_advice(age, retirement_age, risk_profile, corpus):
    prompt = (
        f"I'm {age} years old and want to retire at {retirement_age}. "
        f"My risk profile is {risk_profile}. I need ₹{corpus:,.2f} corpus. "
        "Give me a savings and investment strategy."
    )
    response = model.generate_content(prompt)
    return response.text