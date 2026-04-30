# 🏙️ RepareAqui - Colaborando juntos para uma cidade melhor

## 📖 Sobre o Projeto
Projeto interdisciplinar unindo **Arquitetura, Urbanismo, Análise de Sistemas e Engenharia de Dados**, focado no paradigma das **Smart Cities**. A plataforma permite o mapeamento colaborativo de infraestrutura urbana (Web GIS) e a análise em lote (Batch Processing) dessas ocorrências na nuvem.

## 🛠️ Tecnologias Utilizadas
- **Frontend (Web GIS):** HTML5, CSS3, JavaScript, Leaflet.js, OpenStreetMap.
- **Backend (API & Persistência):** Python, Flask, SQLite.
- **Data Analytics (Big Data):** PySpark, Databricks (Serverless Compute).

## 🗺️ Arquitetura e Passos de Desenvolvimento
1. **O Mapa Básico:** Renderização cartográfica com Leaflet. ✅
2. **A Interação:** Captura de coordenadas e formulários dinâmicos. ✅
3. **O Backend:** API REST com Flask. ✅
4. **Persistência de Dados:** Modelagem em banco SQLite (`INSERT` e `SELECT`). ✅
5. **Visualização Georreferenciada:** Renderização em tempo real de marcadores no mapa. ✅
6. **Módulo Analítico (Data Pipeline):** Script de extração de dados locais (SQLite para CSV) e processamento em nuvem utilizando PySpark para gerar métricas e visualizações interativas (`display()`) de zeladoria urbana. ✅

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.12+
- Git

### Configuração Inicial
1. Clone o repositório:
   `git clone https://github.com/fau-pereira/repare-aqui-webgis.git`
2. Acesse a pasta do projeto e crie o ambiente virtual:
   `python3 -m venv venv`
3. Ative o ambiente virtual:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Instale as dependências:
   `pip install flask`

### Executando a Aplicação
1. Com o ambiente ativado, inicie o servidor:
   `python app.py`
2. Acesse `http://127.0.0.1:5000` no seu navegador. O banco de dados SQLite será criado automaticamente na primeira execução.

## 📊 Como Executar o Módulo de Análise (Databricks)
1. Execute `python exportar_dados.py` para gerar o dataset atualizado (`ocorrencias.csv`).
2. Acesse sua conta no Databricks Workspace (Free Edition).
3. Faça o upload do arquivo CSV para o seu Workspace.
4. Importe o código `automacao_servidor.py` para um Notebook e execute as células para visualizar os gráficos de incidência.
