from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from utils.gemini_client import consulta_gemini
from utils.api_dados import buscar_cursos
from data.contudo import carregar_conteudos
from data.contudo import carregar_noticias
from data.bolsa_vest_int import fetch_bolsas_markdown
from utils.refinamento_prompt import otimizar_prompt_e_modelo
from utils.memoria import summarize_relevant_history
from datetime import datetime
from markdown import markdown
#| agentes |------------------------|
from utils.agents_classificador import is_task
from utils.agents_exatas import exatas_remota
from utils.agents_classificador_ciencias import classify_area
from utils.agents_humanas import humanas_remota

app = Flask(__name__)

# Instruções fixas para o chatbot
from datetime import datetime

def get_system_instructions() -> str:
    agora = datetime.now()
    data = agora.strftime('%Y-%m-%d')
    dia_semana = agora.strftime('%A')
    semana_iso = agora.isocalendar()[1]
    mes = agora.strftime('%B')
    hora = agora.strftime('%H:%M')
    noticias = carregar_noticias()
    URL = "https://partiuintercambio.org/bolsas-de-estudo/#google_vignette"
    bolsas = fetch_bolsas_markdown(URL)

    return f"""\
            Idealizador do projeto autor: Laredo Nunes, para o projeto da escola: Alura, ano: 2025
            Você é um **assistente educacional** especializado em ajudar **jovens brasileiros** a ingressarem na universidade.
            
            📅 **Data:** {data} ({dia_semana})  
            🔢 **Semana ISO:** {semana_iso}  
            🌙 **Mês:** {mes}  
            ⏰ **Hora:** {hora} (America/Sao_Paulo)
            
            📰 **Notícias recentes:**  
            {noticias}
            
            **bolsas de estudo e intercambio recentes:**
            {bolsas}
            
            **Instruções para as respostas:**  
            1. Baseie-se no contexto temporal e nas notícias acima.  
            2. Forneça informações sobre **vestibulares**, **ENEM**, **bolsas de estudo**, **cursos** e **processos seletivos**.  
            3. Estruture a resposta de forma clara: use tópicos, bullets ou passos.  
            4. Seja acolhedor, objetivo e utilize linguagem simples em português.
            
            **Pergunta do usuário:** {{pergunta}}
            """


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/inicio')
def index1():
    return render_template('index.html')


CONTEUDOS = carregar_conteudos()

@app.route('/perguntar', methods=['POST'])
def perguntar():
    pergunta = request.form.get('pergunta')
    print(f'a pergunta feita é: {pergunta}')
    if pergunta is None:
        html_response = markdown('', extensions=["fenced_code", "tables"])
        return render_template('index.html', resposta_html=html_response)
    if is_task(pergunta):
        print('é uma questão')
        literal = classify_area(pergunta)
        print(literal)
        if literal == 'EXATAS':
            retorno = exatas_remota(pergunta)
            print('feito calculo com agente')
            html_response = markdown(retorno, extensions=["fenced_code", "tables"])
            return render_template('index.html', resposta_html=html_response)
        if literal == 'HUMANAS':
            retorno = humanas_remota(pergunta)
            print('feito calculo com agente')
            html_response = markdown(retorno, extensions=["fenced_code", "tables"])
            return render_template('index.html', resposta_html=html_response)
    context_summary = summarize_relevant_history(pergunta)
    print(context_summary)
    prompt_ref, modelo = otimizar_prompt_e_modelo(pergunta) # refina o prompt
    print('-'*90)
    print(prompt_ref)
    print(modelo)
    contexto = "\n".join([f"{k.upper()}: {v}" for k, v in CONTEUDOS.items()])
    prompt = f"""\               
            
                📚 Contexto adicional:
                {get_system_instructions()}{contexto}
            
                🕘 Histórico do usuário:
                {context_summary}
            
                ❓ Pergunta do usuário:
                {prompt_ref}
            """
    resposta = consulta_gemini(prompt, modelo)
    html_response = markdown(resposta, extensions=["fenced_code", "tables"])

    return render_template('index.html', resposta_html=html_response)


@app.route('/cursos', methods=['GET'])
def cursos():
    api_url = "https://api.universidades.gov.br/cursos"
    dados = buscar_cursos(api_url)
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
