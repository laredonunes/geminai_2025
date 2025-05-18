import uuid
import google.generativeai as genai
from google.genai import types
from config import get_env_var
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from typing import Optional

# --- Configuração inicial ---
#API_KEY = get_env_var("API_KEY")
API_KEY = 'AIzaSyDc1E_5mhq34SNdUlAlCEY5xFP21rdiWzc'
genai.configure(api_key=API_KEY)

# Agora usamos a versão numerada que existe na registry
FAST_MODEL = "gemini-1.5-flash-001"

_session_service = InMemorySessionService()

def _make_content(text: str) -> types.Content:
    return types.Content(
        role="user",
        parts=[types.Part(text=text)]
    )

_search_runner = Runner(
    app_name="chatbot_busca",
    agent=LlmAgent(
        name="search_agent",
        model=FAST_MODEL,
        instruction="""
Quando o usuário pedir para 'buscar X' ou 'pesquisar X', use a ferramenta google_search(X)
e retorne um breve resumo dos resultados.
Caso contrário, retorne 'NO_SEARCH'.
""",
        tools=[google_search]
    ),
    session_service=_session_service
)

def search_web(prompt: str, user_id: str = "default_user") -> Optional[str]:
    # Cria sessão
    session = _session_service.create_session(
        app_name="chatbot_busca",
        user_id=user_id,
        state={}
    )
    # Roda o agente
    events = _search_runner.run(
        user_id=user_id,
        session_id=session.id,
        new_message=_make_content(prompt)
    )
    # Pega a resposta final
    for ev in events:
        if ev.is_final_response():
            text = ev.content.parts[0].text.strip()
            return None if text.upper() == "NO_SEARCH" else text
    return None

# Exemplo de uso
if __name__ == "__main__":
    exemplos = [
        "Olá, tudo bem?",
        "por favor, pesquisar notícias sobre mudanças climáticas",
        "listar minhas tarefas internas",
        "buscar tutorial de Flask + Tailwind"
    ]
    for p in exemplos:
        print(f">>> {p!r}\n→ {search_web(p)}\n")

