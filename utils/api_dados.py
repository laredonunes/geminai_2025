import requests

def buscar_cursos(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return {"erro": "não foi possível obter os dados"}
