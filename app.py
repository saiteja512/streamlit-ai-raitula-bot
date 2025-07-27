import streamlit as st
from googletrans import Translator
import requests

# Set up Streamlit app
st.set_page_config(page_title="🌾 రైతుల కోసం AI సహాయకుడు", layout="centered")
st.title("🌾 రైతుల కోసం AI చాట్‌బాట్")
st.write("తెలుగులో మీ వ్యవసాయ ప్రశ్నలకు మద్దతుగా AI")

# Translator setup
translator = Translator()

# Get user input
user_input = st.text_input("మీ ప్రశ్నను తెలుగులో నమోదు చేయండి:")

# Translation: Telugu ➡️ English
def translate_to_english(text):
    try:
        translated = translator.translate(text, src='te', dest='en')
        return translated.text
    except Exception as e:
        return f"Translation Failed: {str(e)}"

# Translation: English ➡️ Telugu
def translate_to_telugu(text):
    try:
        translated = translator.translate(text, src='en', dest='te')
        return translated.text
    except Exception as e:
        return f"Translation Failed: {str(e)}"

# AI call to Ollama via HTTP API
def get_ai_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from model.")
        else:
            return f"Ollama API Error: {response.text}"
    except Exception as e:
        return f"AI Error: {str(e)}"

# Process user input
if user_input:
    with st.spinner("సమాధానం సిద్ధం అవుతోంది..."):
        # Step 1: Translate Telugu to English
        english_prompt = translate_to_english(user_input)

        # Step 2: Get AI response in English
        ai_response_english = get_ai_response(english_prompt)

        # Step 3: Translate AI response back to Telugu
        ai_response_telugu = translate_to_telugu(ai_response_english)

        # Step 4: Show final response
        st.success(ai_response_telugu)
