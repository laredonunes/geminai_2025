import os


def carregar_conteudos():
    conteudos = {}
    for nome in ['bolsas', 'enem', 'universidades']:
        caminho = f"data/{nome}.txt"
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudos[nome] = f.read()
        else:
            conteudos[nome] = f"Conteúdo de {nome} não disponível."
    return conteudos
