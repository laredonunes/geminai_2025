import google.generativeai as genai
from config import get_env_var
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from typing import Optional

# Configure API client once
genai.configure(api_key=get_env_var("GOOGLE_API_KEY"))

FAST_MODEL = "models/gemini-1.5-flash-latest"
# Consider isolating sessions per agent if you need separate conversation state
session_service = InMemorySessionService()

# Agent to classify tasks (true/false)
# BUG FIX: removed invalid app_name parameter from Runner
_task_runner = Runner(
    agent=LlmAgent(
        name="task_classifier",
        model=FAST_MODEL,
        instruction="""
Avalie se a entrada do usuário indica:
- Uma tarefa interna (ex.: adicionar conteúdo, limpar cache)
- Ou uma busca na internet (ex.: 'buscar X', 'pesquisar Y')
Retorne apenas 'true' para tarefa ou busca, caso contrário 'false'.
"""
    ),
    session_service=session_service
)

def is_task(prompt: str) -> bool:
    """
    Usa o agente para classificar se a entrada é uma tarefa.
    Retorna True/False baseando-se na resposta do agente.
    """
    try:
        events = _task_runner.run(
            user_id="default_user",
            session_id="default_session",
            new_message=prompt
        )
        # Extrai resposta final do primeiro evento final
        for event in events:
            if hasattr(event, 'is_final_response') and event.is_final_response():
                text = event.content.parts[0].text
                return text.strip().lower() == 'true'
    except Exception:
        return False
    return False

# Agent to perform web searches
_search_runner = Runner(
    agent=_task_runner.agent,  # reusa o mesmo modelo com instrução ajustada
    session_service=session_service
)

def perform_search(prompt: str) -> Optional[str]:
    """Retorna o resultado da busca ou None se não aplicável."""
    try:
        events = _search_runner.run(
            user_id="default_user",
            session_id="default_session",
            new_message=prompt
        )
        for event in events:
            if hasattr(event, 'is_final_response') and event.is_final_response():
                text = event.content.parts[0].text.strip()
                return None if not text or text.upper() == 'NO_SEARCH' else text
    except Exception:
        return None
    return None

# ... restante do arquivo permanece igual ...(prompt: str) -> Optional[str]:
    # Cache this function if high-frequency searches are expected
    try:
        result = _search_runner.run(prompt)
    except Exception:
        return None
    text = result.strip()
    return None if text.upper() == 'NO_SEARCH' or not text else text

if __name__ == "__main__":
    # Fixed indentation and variable naming for clarity
    prompt_text = 'matematica'
    search_text = perform_search(prompt_text)
    print(search_text)


