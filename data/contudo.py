import os
from cachetools import cached, TTLCache
from data.rss_uol import salvar_rss_em_md

# Cache com 1 entrada e expira após 300 segundos (5 minutos)
conteudos_cache = TTLCache(maxsize=1, ttl=300)
noticias_cache = TTLCache(maxsize=1, ttl=36000)

@cached(conteudos_cache)
def carregar_conteudos():
    conteudos = {}
    pasta = 'data'

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho) and arquivo.endswith('.md'):
            nome = os.path.splitext(arquivo)[0]
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudos[nome] = f.read()

    return conteudos

@cached(noticias_cache)
def carregar_noticias():
    conteudos = {}
    pasta = 'data/noticias'
    salvar_rss_em_md(
        url_rss="https://rss.uol.com.br/feed/vestibular.xml",
        arquivo_md=f"{pasta}/vestibular_feed.md"
    )

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho) and arquivo.endswith('.md'):
            nome = os.path.splitext(arquivo)[0]
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudos[nome] = f.read()

    return conteudos