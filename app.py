#Inicio de APP
import json
from flask import Flask, flash, redirect, render_template, request, jsonify, send_file, session, url_for
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
from io import BytesIO
import base64

try:
  print("Sucesso na Ligação ")
except Exception as e:
  print("Falha de ligacao new APP")

  conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=ASUSTUFGAMING\EI28235;'
    r'DATABASE=poppets1;'
    r'UID=sa;'
    r'PWD=123456;'
)

'''
# Estabeleça a conexão
conn = pyodbc.connect(conn_str)

# Crie um cursor para executar consultas SQL
cursor = conn.cursor()

# Exemplo de consulta
cursor.execute("SELECT idPieza, pPoppetpos, ts FROM poppet")
rows = cursor.fetchall()

# Iterar sobre os resultados
for row in rows:
    print(row.idPieza, row.pPoppetpos, row.ts)

# Feche a conexão e o cursor quando terminar
cursor.close()
conn.close()
'''


# Estabeleça a conexão
# Função para gerar o gráfico
def generate_plot():
    # Estabeleça a conexão
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=ASUSTUFGAMING\EI28235;'
        r'DATABASE=poppets1;'
        r'UID=sa;'
        r'PWD=123456;'
    )
    conn = pyodbc.connect(conn_str)

    # Execute a consulta SQL para obter os dados
    query = "SELECT idPieza, pPoppetpos, ts FROM poppet"
    data = pd.read_sql(query, conn)

    # Feche a conexão após a obtenção dos dados
    conn.close()

    # Converta a coluna 'ts' para datetime
    data['ts'] = pd.to_datetime(data['ts'])

    # Resample dos dados por ano para calcular a média anual de pPoppetpos
    yearly_data = data.resample('Y', on='ts')['pPoppetpos'].mean()

    # Crie o gráfico da série temporal
    plt.figure(figsize=(12, 6))  # Ajuste o tamanho da figura conforme necessário
    plt.plot(yearly_data.index, yearly_data.values, marker='o', linestyle='-')

    # Defina os rótulos e o título com uma reflexão precisa do eixo y
    plt.xlabel('Ano')
    plt.ylabel('Média de pPoppetpos')
    plt.title('Média de pPoppetpos por Ano')

    # Gire os rótulos do eixo x para melhor legibilidade, se necessário
    plt.xticks(rotation=45)  # Ajuste o ângulo de rotação conforme necessário

    plt.grid(True)
    
    # Salvar o gráfico como uma imagem
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode()
    buffer.close()
    
    # Retorne os dados do gráfico
    return graph




app = Flask(__name__)
app.secret_key = 'secretkeysparepartscroston'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/graph')
def graph():
    graph = generate_plot()
    return render_template('graph.html', graph=graph)


if __name__ == "__main__":
    app.run(debug=True)