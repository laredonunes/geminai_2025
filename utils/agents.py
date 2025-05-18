import google.generativeai as genai
from config import get_env_var

# Carrega a API key
API_KEY = get_env_var("API_KEY")
genai.configure(api_key=API_KEY)

# Modelo rápido para classificação
FAST_MODEL = "models/gemini-1.5-flash-latest"

# Instruções para o classificador de tarefas
TASK_INSTRUCTION = """
                        Você recebe uma entrada do usuário. Avalie se é uma TAREFA que o sistema deve executar
                        (ex.: adicionar conteúdo, gerar arquivo, limpar cache) ou se o usuário deseja
                        que você realize uma busca na internet por um assunto específico
                        (ex.: "buscar X", "pesquisar sobre Y").
                        
                        Se for tarefa interna ou busca na internet, responda exatamente "true".
                        Se for dúvida apenas sobre vestibular, ENEM ou qualquer outro tópico fora de escopo, responda exatamente "false".
                        
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

