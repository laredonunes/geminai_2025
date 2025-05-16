import google.generativeai as genai
from datetime import datetime
from config import get_env_var

# Configure sua API key
genai.configure(api_key=get_env_var("API_KEY"))

# Modelos disponíveis
FAST_REFINER   = 'models/gemini-1.5-flash-latest'       # muito rápido para tarefas leves
HIGH_ACCURACY  = 'models/gemini-2.5-pro-preview-05-06'  # alta precisão para resposta final

def otimizar_prompt_e_modelo(pergunta: str) -> tuple[str, str]:
    """
    1) Usa um modelo rápido para refinar o prompt original.
    2) Escolhe o modelo ideal para a resposta final (velocidade vs. precisão).
    Retorna (prompt_refinado, nome_do_modelo_recomendado).
    """
    # 1️⃣ Etapa de refino do prompt
    refiner = genai.GenerativeModel(FAST_REFINER)
    open_prompt = f"""
                    Refine este prompt para deixá-lo mais claro e objetivo,
                    incluindo contexto temporal e notícias recentes:
                    ---
                    {pergunta}
                    **Mantenha a intenção original**, mesmo que o texto de entrada seja muito curto.
                    **Retorne somente** o prompt refinado, sem solicitar informações adicionais ao usuário.
                    """
    resposta_refino = refiner.generate_content(open_prompt)
    prompt_refinado = resposta_refino.text.strip()

    # 2️⃣ Escolha de modelo
    # Aqui você pode usar heurísticas: tamanho do prompt, urgência, etc.
    # Exemplo simples: se o prompt refinado for curto → modelo rápido; caso contrário → alta precisão.
    if len(prompt_refinado) < 200:
        modelo_recomendado = FAST_REFINER
    else:
        modelo_recomendado = HIGH_ACCURACY

    return prompt_refinado, modelo_recomendado

'''
# Exemplo de uso:
user_q = "Quais bolsas do ProUni estão abertas esta semana?"
prompt_ref, modelo = otimizar_prompt_e_modelo(user_q)
print("Prompt refinado:\n", prompt_ref)
print("Use o modelo:", modelo)

# Na sua rota Flask, bastaria:
# resposta = genai.GenerativeModel(modelo).generate_content(prompt_ref).text

'''

