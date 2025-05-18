import logging
import google.generativeai as genai
from config import get_env_var
from typing import Any

# Configuração da API
API_KEY = get_env_var("API_KEY")
genai.configure(api_key=API_KEY)

# Modelos
FAST_MODEL     = "models/gemini-1.5-flash-latest"
SIMPLE_MODEL   = "models/gemini-1.5-flash-latest"
COMPLEX_MODEL  = "models/gemini-2.5-pro-preview-05-06"
REVIEW_MODEL   = "models/gemini-1.5-flash-latest"
DIDACTIC_MODEL = "models/gemini-1.5-flash-latest"

MAX_RETRIES = 3

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

class BaseAgent:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def run(self, prompt: str) -> str:
        logging.info(f"Chamando modelo `{self.model_name}`")
        return self.model.generate_content(prompt).text.strip()

class ClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(FAST_MODEL)
        self.task_instruction = """
                                    Você recebe uma entrada do usuário...
                                    Se for problema de exatas, responda EXACTLY: exatas
                                    Caso contrário, responda EXACTLY: outro
                                    """

    def is_math(self, text: str) -> bool:
        prompt = f"{self.task_instruction}\nTexto: ---{text}---"
        resposta = self.run(prompt).lower()
        logging.info(f"Classificação exatas? → {resposta}")
        return resposta == "exatas"

    def complexity(self, text: str) -> str:
        prompt = f"""
Classifique este problema de exatas em ‘simples’ ou ‘complexa’.
Texto: ---{text}---
"""
        resposta = self.run(prompt).lower()
        logging.info(f"Complexidade detectada → {resposta}")
        return resposta

class MathAgent(BaseAgent):
    def solve(self, problem: str) -> str:
        prompt = f"Resolva passo a passo:\n---{problem}---"
        solution = self.run(prompt)
        logging.info("Solução gerada")
        return solution

class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(REVIEW_MODEL)

    def verify(self, solution: str) -> bool:
        prompt = f"Verifique se este cálculo e resposta estão corretos:\n---{solution}---\nRetorne apenas 'ok' ou 'erro'."
        resposta = self.run(prompt).lower()
        logging.info(f"Resultado da revisão → {resposta}")
        return resposta == "ok"

class DidacticAgent(BaseAgent):
    def __init__(self):
        super().__init__(DIDACTIC_MODEL)

    def make_didactic(self, solution: str) -> str:
        prompt = (f"Voce é o instrutor de exatas e esta recebendo o texto com a solução de um problema de exatas"
                  f"Torne este texto mais didático e claro para o usuário:\n---{solution}---")
        texto = self.run(prompt)
        logging.info("Texto final didático gerado")
        return texto

class PipelineAgent:
    def __init__(self):
        self.clf     = ClassifierAgent()
        self.simple  = MathAgent(SIMPLE_MODEL)
        self.complex = MathAgent(COMPLEX_MODEL)
        self.review  = ReviewAgent()
        self.didactic= DidacticAgent()

    def handle(self, user_input: str) -> str:
        print("🔍 [1/5] Verificando se é questão de exatas...")
        if not self.clf.is_math(user_input):
            print("❌ Não é um problema de exatas.")
            return "Desculpe, só consigo resolver questões de exatas."

        print("⚙️ [2/5] Classificando complexidade...")
        complexity = self.clf.complexity(user_input)
        agent = self.simple if complexity == "simples" else self.complex
        print(f"✅ Complexidade: {complexity}. Usando o agente “{agent.model_name}”.")

        # loop de tentativas
        for attempt in range(1, MAX_RETRIES + 1):
            print(f"🧮 [3/5] Tentativa {attempt} de {MAX_RETRIES}...")
            sol = agent.solve(user_input)
            print(f"→ Solução bruta gerada. Rodando revisão...")
            if self.review.verify(sol):
                print("✅ Cálculo verificado com sucesso.")
                print("✍️ [4/5] Tornando didático...")
                final = self.didactic.make_didactic(sol)
                print("🎯 [5/5] Pronto para exibir ao usuário.")
                return final
            else:
                print("⚠️ Revisão indicou erro. Re-tentando..." if attempt < MAX_RETRIES else "🛑 Limite de tentativas atingido.")

        print("❌ Falha na análise após várias tentativas.")
        return "Falha na análise do cálculo após várias tentativas. Tente reformular sua questão."

def exatas_remota(pergunta):
    pipeline = PipelineAgent()
    resposta = pipeline.handle(pergunta)
    return resposta


if __name__ == "__main__":
    pipeline = PipelineAgent()
    pergunta = input("Digite sua questão de exatas: ")
    resposta = pipeline.handle(pergunta)
    print("\n💬 Resposta final:\n")
    print(resposta)


