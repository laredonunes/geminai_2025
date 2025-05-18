import logging
import google.generativeai as genai
from config import get_env_var

# Configuração da API
API_KEY = get_env_var("API_KEY")
genai.configure(api_key=API_KEY)

# Modelos
FAST_MODEL            = "models/gemini-1.5-flash-latest"         # para classificação
HUMANAS_SIMPLE_MODEL  = "models/gemini-1.5-chat-latest"         # tarefas humanas “simples”
HUMANAS_COMPLEX_MODEL = "models/gemini-2.5-pro-preview-05-06"    # tarefas humanas “complexas”
HUMANAS_REVIEW_MODEL  = "models/gemini-1.5-flash-latest"         # revisão
HUMANAS_DIDACTIC_MODEL= "models/gemini-1.5-flash-latest"         # didatização

MAX_RETRIES = 3

# Logging
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

class ClassifierAgentHumanas(BaseAgent):
    INSTRUCTION = """
Você recebe uma entrada do usuário. Avalie se ela é uma QUESTÃO de prova/simulado e,
em caso afirmativo, determine se pertence a HUMANAS (história, filosofia, geografia, etc.)

• Se for questão de HUMANAS, responda EXACTLY: HUMANAS  
• Se não for questão de simulado ou pertencer a outra área, responda EXACTLY: OUTRO

Retorne apenas HUMANAS ou OUTRO.
"""
    def __init__(self):
        super().__init__(FAST_MODEL)

    def is_humanas(self, text: str) -> bool:
        prompt = f"{self.INSTRUCTION}\nTexto: ---{text}---"
        resp = self.run(prompt).upper()
        logging.info(f"Classificação HUMANAS? → {resp}")
        return resp == "HUMANAS"

    def complexity(self, text: str) -> str:
        prompt = f"""
Classifique esta questão de HUMANAS em ‘simples’ ou ‘complexa’.
Texto: ---{text}---
"""
        resp = self.run(prompt).lower()
        logging.info(f"Complexidade HUMANAS detectada → {resp}")
        return resp

class HumanasAgent(BaseAgent):
    def solve(self, question: str) -> str:
        prompt = f"Responda detalhadamente:\n---{question}---"
        sol = self.run(prompt)
        logging.info("Resposta humana gerada")
        return sol

class ReviewAgentHumanas(BaseAgent):
    def __init__(self):
        super().__init__(HUMANAS_REVIEW_MODEL)

    def verify(self, text: str) -> bool:
        prompt = f"Verifique se esta resposta de HUMANAS está completa e correta:\n---{text}---\nRetorne apenas 'ok' ou 'erro'."
        resp = self.run(prompt).lower()
        logging.info(f"Revisão HUMANAS → {resp}")
        return resp == "ok"

class DidacticAgentHumanas(BaseAgent):
    def __init__(self):
        super().__init__(HUMANAS_DIDACTIC_MODEL)

    def make_didactic(self, text: str) -> str:
        prompt = f"Torne este texto de HUMANAS mais didático e acessível:\n---{text}---"
        did = self.run(prompt)
        logging.info("Texto HUMANAS didático gerado")
        return did

class PipelineAgentHumanas:
    def __init__(self):
        self.clf      = ClassifierAgentHumanas()
        self.simple   = HumanasAgent(HUMANAS_SIMPLE_MODEL)
        self.complex  = HumanasAgent(HUMANAS_COMPLEX_MODEL)
        self.review   = ReviewAgentHumanas()
        self.didactic = DidacticAgentHumanas()

    def handle(self, user_input: str) -> str:
        print("🔍 [1/5] Verificando se é questão de HUMANAS...")
        if not self.clf.is_humanas(user_input):
            print("❌ Não é uma questão de HUMANAS.")
            return "Desculpe, só consigo resolver questões de HUMANAS."

        print("⚙️ [2/5] Classificando complexidade (Humanas)...")
        complexity = self.clf.complexity(user_input)
        agent = self.simple if complexity == "simples" else self.complex
        print(f"✅ Complexidade: {complexity}. Usando o agente “{agent.model_name}”.")

        for attempt in range(1, MAX_RETRIES + 1):
            print(f"📝 [3/5] Tentativa {attempt} de {MAX_RETRIES} para resposta...")
            sol = agent.solve(user_input)
            print("→ Resposta bruta gerada. Fazendo revisão...")
            if self.review.verify(sol):
                print("✅ Revisão ok.")
                print("✍️ [4/5] Tornando didático...")
                final = self.didactic.make_didactic(sol)
                print("🎯 [5/5] Pronto para exibir ao usuário.")
                return final
            else:
                msg = "⚠️ Revisão indicou erro. Retentando..." if attempt < MAX_RETRIES else "🛑 Limite de tentativas atingido."
                print(msg)

        print("❌ Falha na análise após várias tentativas.")
        return "Falha na resposta de HUMANAS após várias tentativas. Tente reformular sua questão."

def humanas_remota(pergunta: str) -> str:
    pipeline = PipelineAgentHumanas()
    return pipeline.handle(pergunta)

if __name__ == "__main__":
    pipeline = PipelineAgentHumanas()
    pergunta = input("Digite sua questão de HUMANAS: ")
    resposta = pipeline.handle(pergunta)
    print("\n💬 Resposta final:\n")
    print(resposta)
