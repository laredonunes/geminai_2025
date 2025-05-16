import feedparser
from datetime import datetime

def salvar_rss_em_md(url_rss: str, arquivo_md: str):
    feed = feedparser.parse(url_rss)

    linhas = []
    linhas.append(f"# Feed: {feed.feed.title}\n")
    linhas.append(f"> Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    for entry in feed.entries:
        titulo = entry.title
        link = entry.link
        publicado = entry.published
        descricao = entry.summary

        linhas.append(f"## {titulo}\n")
        linhas.append(f"- 📅 Publicado: {publicado}")
        linhas.append(f"- 🔗 [Link]({link})\n")
        linhas.append(f"{descricao}\n")
        linhas.append("---\n")

    with open(arquivo_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(linhas))

    print(f"Arquivo {arquivo_md} salvo com sucesso!")

