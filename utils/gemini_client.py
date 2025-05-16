import requests
import google.generativeai as genai
from config import get_env_var

genai.configure(api_key=get_env_var("API_KEY"))

#MODEL_NAME = 'models/gemini-2.5-pro-preview-05-06'

def consulta_gemini(prompt: str, MODEL_NAME) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text

