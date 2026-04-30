import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def inicializar_banco():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descricao TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

inicializar_banco()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_ocorrencia():
    dados = request.get_json()
    tipo = dados.get('tipo')
    descricao = dados.get('descricao')
    latitude = dados.get('latitude')
    longitude = dados.get('longitude')
    
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO ocorrencias (tipo, descricao, latitude, longitude)
        VALUES (?, ?, ?, ?)
    ''', (tipo, descricao, latitude, longitude))
    conexao.commit()
    conexao.close()
    
    return jsonify({"mensagem": "Ocorrência salva com sucesso no Banco de Dados!"}), 201

# Quando o mapa carregar, ele vai acessar esta rota para pedir os dados salvos
@app.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    conexao = sqlite3.connect('banco.db')
    
    # Configura o banco para retornar os dados como "dicionários" (facilita para transformar em JSON)
    conexao.row_factory = sqlite3.Row 
    cursor = conexao.cursor()
    
    # O comando SQL 'SELECT *' pega TUDO que está na tabela
    cursor.execute('SELECT * FROM ocorrencias')
    linhas = cursor.fetchall()
    
    # Transforma as linhas do banco de dados em uma lista que o JavaScript consegue ler
    lista_ocorrencias = [dict(linha) for linha in linhas]
    
    conexao.close()
    
    # Envia a lista completa de volta para o mapa
    return jsonify(lista_ocorrencias)

if __name__ == '__main__':
    app.run(debug=True, port=5000)