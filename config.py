# config.py
import os
from dotenv import load_dotenv, find_dotenv

def get_env_var(key: str) -> str:
    env_path = find_dotenv()
    if env_path:
        load_dotenv(env_path, override=False)
    val = os.getenv(key)
    if val is None:
        raise RuntimeError(f"Variável de ambiente '{key}' não encontrada.")
    return val
