import google.generativeai as genai
import os

GOOGLE_API_KEY = "AIzaSyCHG-rdeaWlrDa8Woe_BssfQuLyRsOBv50"  # Replace with your actual Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def ask_question_about_listing(listing_text, user_question):
    prompt = f"""
You are a real estate investment advisor.

Listing:
{listing_text}

Question:
{user_question}

Respond as if advising an investor.
"""
    response = model.generate_content(prompt)
    return response.text
