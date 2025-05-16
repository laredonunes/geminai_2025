import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# cache interno
_cache = {
    'timestamp': None,
    'value': None
}

def fetch_bolsas_markdown(url: str) -> str:
    """
    Busca todas as notícias na grade de bolsas de estudo do site e
    retorna um texto em Markdown. Usa cache de 3 horas para não
    requisitar a cada chamada.
    """
    now = datetime.now()
    # se houver valor em cache e não tiver expirado (<3h), retorna cache
    if _cache['timestamp'] and (now - _cache['timestamp'] < timedelta(hours=3)):
        return _cache['value']

    # caso contrário, faz o scraping
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    items = soup.select('div.jet-listing-grid__item')

    md_lines = []
    for item in items:
        date_el = item.select_one('.jet-listing-dynamic-field__content')
        date = date_el.get_text(strip=True) if date_el else None

        link_el = item.select_one('.jet-listing-dynamic-link__link')
        title = link_el.get_text(strip=True) if link_el else 'Sem título'
        link = link_el['href'] if link_el and link_el.has_attr('href') else '#'

        cats = [a.get_text(strip=True) for a in item.select('.jet-listing-dynamic-terms__link')]

        style = item.find('style', text=re.compile(r'background-image'))
        img_url = None
        if style:
            m = re.search(r'url\("([^"]+)"\)', style.string)
            if m:
                img_url = m.group(1)

        md_lines.append(f"### [{title}]({link})")
        if date:
            md_lines.append(f"- **Data:** {date}")
        if cats:
            md_lines.append(f"- **Categorias:** {', '.join(cats)}")
        if img_url:
            md_lines.append(f"- ![]({img_url})")
        md_lines.append("")

    result = "\n".join(md_lines)
    # atualiza cache
    _cache['timestamp'] = now
    _cache['value'] = result
    return result


if __name__ == "__main__":
    URL = "https://partiuintercambio.org/bolsas-de-estudo/#google_vignette"
    print(fetch_bolsas_markdown(URL))
