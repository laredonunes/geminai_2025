import os
import json
from datetime import datetime
import google.generativeai as genai
from config import get_env_var

# Configuração
genai.configure(api_key=get_env_var("API_KEY"))
FAST_MODEL   = 'models/gemini-1.5-flash-latest'
MEMORY_FILE  = 'user_memory_st.json'
MAX_HISTORY  = 100

def summarize_relevant_history(prompt: str) -> str:
    """
    1) Garante que o arquivo existe (cria [] se não existir).
    2) Carrega o histórico atual.
    3) Extrai as últimas MAX_HISTORY entradas como contexto.
    4) Adiciona a nova interação ao arquivo.
    5) Chama o modelo rápido para gerar o resumo do contexto anterior.
    """
    # 1) Cria o arquivo vazio se não existir
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    # 2) Carrega tudo
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        try:
            memory = json.load(f)
        except json.JSONDecodeError:
            memory = []

    # 3) Prepara o contexto: apenas as últimas MAX_HISTORY entradas
    history = memory[-MAX_HISTORY:]

    # 4) Atualiza a memória com este prompt
    new_record = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt
    }
    memory.append(new_record)
    # mantém só as últimas MAX_HISTORY
    memory = memory[-MAX_HISTORY:]
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

    # 5) Monta o texto do histórico para o resumo
    history_lines = [
        f"[{rec['timestamp'][:19]}] {rec['prompt'].replace(chr(10), ' ')}"
        for rec in history
    ]
    history_text = "\n".join(history_lines) if history_lines else "— nenhum histórico —"

    # 6) Gera o resumo com o modelo rápido
    summary_prompt = f"""
                        Você é um assistente que faz um breve **resumo de contexto**.
                        Aqui está o histórico das últimas interações (máx. {MAX_HISTORY} registros):
                        
                        {history_text}
                        
                        Dada a nova pergunta do usuário:
                        \"\"\"{prompt}\"\"\"
                        
                        Forneça um **resumo conciso** (máx. 5 linhas) dos pontos do histórico que são **mais relevantes** para ajudar a responder essa pergunta.
                    """

    model = genai.GenerativeModel(FAST_MODEL)
    resp = model.generate_content(summary_prompt)
    return resp.text.strip()


