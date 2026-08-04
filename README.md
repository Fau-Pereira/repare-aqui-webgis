# 🏙️ RepareAqui - Colaborando juntos para uma cidade melhor

**Versão:** 1.1.0 (Atualização: Agente de IA Integrado)

O **RepareAqui** é uma plataforma WebGIS voltada para cidades inteligentes (Smart Cities). O sistema permite que cidadãos relatem problemas de infraestrutura urbana diretamente em um mapa interativo, enquanto a gestão municipal (Prefeitura) acompanha os dados através de um painel corporativo com mapas de calor (Heatmaps) e triagem automatizada.

## ✨ Novidades da Versão 1.1.0
* **Triagem com Inteligência Artificial:** Integração com LLM (Google Gemini) via LangChain. Agora, ao relatar um problema, um Agente de IA analisa a descrição em texto livre, classifica o nível de urgência e sugere automaticamente a secretaria municipal responsável.
* **Protocolo Indestrutível:** Novo sistema de geração de protocolos únicos baseados em *timestamp*.
* **Proteção de Sessão (Clean Code):** Implementação de *Rollback* automático no banco de dados em caso de falhas na API externa, garantindo resiliência do sistema.

## 🛠️ Tecnologias Utilizadas

**Frontend (Cidadão e Painel Corporativo)**
* React.js (com Vite)
* Leaflet & React-Leaflet (WebGIS)
* Leaflet.heat (Mapa de Calor de Densidade Urbana)
* Axios (Consumo de API)

**Backend (API Restful)**
* Python 3 (Flask)
* SQLAlchemy (ORM)
* LangChain & Google Generative AI (Agente Despachante)
* PostgreSQL (Banco de Dados)

## 🚀 Como Rodar o Projeto Localmente

### Pré-requisitos
* Node.js instalado
* Python 3.10+ instalado
* PostgreSQL rodando (via Docker ou instalação nativa)

### 1. Configurando o Banco de Dados
Certifique-se de ter um banco de dados PostgreSQL rodando na porta `5432` com o nome `repareaqui`.

### 2. Configurando o Backend (API)
Abra um terminal e navegue até a pasta `backend`:
```bash
cd backend
```

Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```
_(Certifique-se de ter as bibliotecas: flask, flask-sqlalchemy, flask-cors, psycopg2-binary, langchain, langchain-google-genai)._

Crie um arquivo .env na pasta backend com as variáveis:
```Snippet de código
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/repareaqui
GOOGLE_API_KEY=sua_chave_do_google_ai_studio
```

Inicie o servidor:
```bash
python run.py
```
_O backend estará rodando na porta 5000._

### 3. Configurando o Frontend (Interface)
Abra um novo terminal e navegue até a pasta 'frontend':
```bash
cd frontend
```

Instale as dependências do Node:
```bash
npm install
```

Inicie o servidor de desenvolvimento:
```bash
npm run dev
```
_O frontend estará disponível no navegador em 'http://localhost:5173'._

## 🗺️ Fluxo de Uso
1. Acesse a aplicação cidadão, clique no mapa e reporte um problema.
2. Acompanhe o terminal do Backend para ver a IA realizando a triagem em tempo real.
3. Acesse a rota corporativa para visualizar os chamados e o Heatmap de incidências (Mapa de Calor).