import google.generativeai as genai
from config import get_env_var

# Carrega a API key
API_KEY = get_env_var("API_KEY")
genai.configure(api_key=API_KEY)

# Modelo rápido para classificação
FAST_MODEL = "models/gemini-1.5-flash-latest"

# Instruções para o classificador de área
TASK_INSTRUCTION = """
Você recebe uma entrada do usuário. Avalie se ela é uma QUESTÃO de prova/simulado e, em caso afirmativo,
determine a qual área pertence:

• Se for uma questão de EXATAS (matemática, física, química, etc.), responda exatamente “EXATAS”.
• Se for uma questão de HUMANAS (história, filosofia, geografia, etc.), responda exatamente “HUMANAS”.
• Se não for uma questão de simulado, responda exatamente “NENHUM”.

Retorne apenas EXATAS, HUMANAS ou NENHUM.
"""

def classify_area(prompt: str) -> str:
    """
    Retorna a string EXATAS, HUMANAS ou NENHUM.
    """
    classifier_prompt = f"{TASK_INSTRUCTION}\nTexto de entrada:\n---{prompt}---"
    model = genai.GenerativeModel(FAST_MODEL)
    answer = model.generate_content(classifier_prompt).text.strip().upper()
    return answer

def is_simulado_de_exatas_ou_humanas(prompt: str) -> bool:
    """
    Retorna True se for questão de EXATAS ou HUMANAS; False caso contrário.
    """
    area = classify_area(prompt)
    return area in ("EXATAS", "HUMANAS")


# Exemplo de uso
if __name__ == "__main__":
    texto = "Explique o que é fotossíntese."
    resultado = classify_area(texto)
    print(f"→ Área detectada: {resultado}")             # “HUMANAS” ou “NENHUM”
    print(is_simulado_de_exatas_ou_humanas(texto))      # True ou False


