import google.generativeai as genai
from config import get_env_var

genai.configure(api_key=get_env_var("API_KEY"))

models = genai.list_models()

for model in models:
    print(model.name, model.supported_generation_methods)
