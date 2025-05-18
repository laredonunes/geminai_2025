import os
import json
from datetime import datetime
from config import get_env_var
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# ---------- Google Calendar Setup ----------
# Usa Service Account para autenticação (JSON key file)
SERVICE_ACCOUNT_FILE = get_env_var("GOOGLE_CALENDAR_SERVICE_ACCOUNT_JSON")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
calendar_service = build('calendar', 'v3', credentials=credentials)

# ---------- ADK Agent: Event Extractor ----------
EXTRACT_INSTRUCTION = """
Você recebe um texto de usuário solicitando criação de evento na agenda.
Extraia e retorne somente um objeto JSON com as seguintes chaves:
- "summary": título do evento
- "description": descrição opcional
- "start": data e hora de início no formato ISO (ex: 2025-06-01T14:00:00)
- "end": data e hora de término no formato ISO
"""
extract_agent = LlmAgent(
    name="calendar_extractor",
    model="models/gemini-1.5-flash-latest",
    instruction=EXTRACT_INSTRUCTION
)
_session = InMemorySessionService()
_extract_runner = Runner(
    app_name="chatbot_universitario_calendar",
    agent=extract_agent,
    session_service=_session
)

def schedule_event(prompt: str) -> dict:
    """
    1) Usa ADK Agent para extrair JSON de evento.
    2) Cria o evento no Google Calendar.
    3) Retorna o objeto do evento criado.
    """
    # Extrai JSON do prompt
    events = _extract_runner.run(user_id="user", session_id="session", new_message=prompt)
    # Pega último evento de extração
    raw = events[-1].content if events else '{}'
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("Não foi possível extrair os dados do evento.")

    event_body = {
        'summary': data.get('summary'),
        'description': data.get('description', ''),
        'start': {'dateTime': data.get('start'), 'timeZone': get_env_var('CALENDAR_TIMEZONE')},
        'end': {'dateTime': data.get('end'), 'timeZone': get_env_var('CALENDAR_TIMEZONE')},
    }
    # Insere no Google Calendar
    created = calendar_service.events().insert(calendarId='primary', body=event_body).execute()
    return created
