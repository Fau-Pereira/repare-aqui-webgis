# Importamos a ferramenta de banco de dados e a ferramenta de arquivos CSV
import sqlite3
import csv

def exportar_para_csv():
    # 1. Conecta ao nosso banco de dados da Smart City
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    # 2. Pega todas as ocorrências salvas
    cursor.execute("SELECT * FROM ocorrencias")
    dados = cursor.fetchall()

    # 3. Pega os nomes das colunas (id, tipo, descricao, latitude, longitude)
    nomes_colunas = [descricao[0] for descricao in cursor.description]

    # 4. Cria e abre um arquivo chamado 'ocorrencias.csv' para escrita ('w')
    with open('ocorrencias.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        
        # Escreve o cabeçalho (nomes das colunas) na primeira linha
        escritor.writerow(nomes_colunas)
        
        # Escreve todos os dados logo abaixo
        escritor.writerows(dados)

    # 5. Fecha a conexão e avisa que terminou
    conexao.close()
    print("✅ Sucesso! O arquivo 'ocorrencias.csv' foi gerado na sua pasta.")

# Executa a função
if __name__ == '__main__':
    exportar_para_csv()