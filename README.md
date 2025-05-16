# Chatbot Universitário (EducAI)

> **Assistente educacional em Python/Flask para vestibulares e ENEM**

---

## 📝 Descrição

O **Chatbot Universitário** (EducAI) é um assistente virtual desenvolvido em Python e Flask, integrado à API **Google Gemini**, que auxilia estudantes brasileiros no processo de preparação para vestibulares e ENEM. O sistema injeta contexto temporal e notícias em tempo real, mantém histórico de conversas e utiliza cache para otimizar o desempenho. A interface, inspirada no estilo TikTok, é responsiva e voltada ao público jovem.

---

## 🚀 Funcionalidades Principais

* **Contexto Dinâmico**: inclui data, hora, semana ISO e notícias recentes no prompt.
* **Pipeline de Prompt**: refinamento rápido e resposta final de alta precisão.
* **Memória de Conversa**: armazena os últimos 100 prompts e gera resumo de histórico relevante.
* **Cache de Conteúdos**: carrega e faz cache de arquivos de conhecimento (por ex. edital, dicas).
* **Interface Mobile-First**: UI escura com design inspirado no TikTok, chat contínuo e carregamento assíncrono.

---

## 📦 Tecnologias

* **Backend**: Python 3.12, Flask
* **AI**: Google Generative AI (Gemini)
* **UI**: Tailwind CSS
* **Cache/Env**: python-dotenv, cachetools
* **RSS**: feedparser

---

## ⚙️ Pré-requisitos

* Python 3.10+ instalado
* Conta e API Key habilitada no Google AI Studio

---

## 💾 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/laredonunes/chatbot-universitario.git
   cd chatbot-universitario
   ```
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Configure suas variáveis de ambiente (no arquivo `.env`):

   ```dotenv
   GOOGLE_API_KEY=SuaChaveAqui
   ```

---

## ▶️ Uso

1. Execute o servidor Flask:

   ```bash
   flask run
   ```
2. Acesse `http://127.0.0.1:5000` no navegador.
3. Na tela de boas‑vindas, clique em **Começar** para ir ao chat.
4. Digite sua pergunta e aguarde a resposta com histórico visível.

---

## 🔧 Configurações

* **Modelos AI**: ajuste `FAST_MODEL` e `HIGH_ACCURACY` em `config.py` ou variáveis de ambiente se desejar usar outros modelos Gemini.
* **Cache TTL**: modifique `TTLCache` em `utils/cache.py` para alterar o tempo de retenção de conteúdo.
* **RSS Feed**: edite a URL em `utils/rss_to_md.py` para outro feed de notícias.

---

## 📡 Endpoints da API

| Rota                  | Método | Descrição                                  |
| --------------------- | ------ | ------------------------------------------ |
| `/`                   | GET    | Página de boas‑vindas                      |
| `/inicio`             | GET    | Interface principal do chat                |
| `/perguntar`          | POST   | Recebe pergunta e retorna resposta em HTML |
| `/sobre`              | GET    | Página com descrição do projeto            |
| `/adicionar_conteudo` | POST   | Adiciona/atualiza arquivo de conhecimento  |

---

## 🤝 Contribuição

Contribuições são bem‑vindas! Siga os passos abaixo:

1. Fork deste repositório.
2. Crie uma branch feature: `git checkout -b feature/nova-funcionalidade`
3. Faça commit das suas alterações: `git commit -m 'Adiciona nova funcionalidade'`
4. Envie para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request relatando sua proposta.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**Laredo Nunes**
GitHub: [laredonunes](https://github.com/laredonunes)
