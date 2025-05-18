import google.generativeai as genai
from config import get_env_var

# Carrega a API key
API_KEY = get_env_var("API_KEY")
genai.configure(api_key=API_KEY)

# Modelo rápido para classificação
FAST_MODEL = "models/gemini-1.5-flash-latest"

# Instruções para o classificador de tarefas
TASK_INSTRUCTION = """
                    Você recebe uma entrada do usuário. Analise se ela é UMA QUESTÃO de prova/simulado
                    pertencente a EXATAS (matemática, física, química, etc.) ou HUMANAS (história, filosofia, geografia, etc.).
                    
                    • Se for uma questão de EXATAS ou HUMANAS, responda exatamente “true”.  
                    • Se for qualquer outro tipo de conteúdo (não é questão de prova ou simulado), responda exatamente “false”.
                    
                    Retorne apenas true ou false.
                    """

def is_task(prompt: str) -> bool:
    """
    Retorna True se o prompt for uma tarefa de sistema; caso contrário, False.
    """
    classifier_prompt = f"""
                            {TASK_INSTRUCTION}
                            
                            Texto de entrada:
                            ---{prompt}---
                        """
    model = genai.GenerativeModel(FAST_MODEL)
    response = model.generate_content(classifier_prompt)
    answer = response.text.strip().lower()
    return answer == 'true'

