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


# Estabeleça a conexão
# Função para gerar o gráfico
def generate_plot(year):
    # Estabeleça a conexão
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=ASUSTUFGAMING\EI28235;'
        r'DATABASE=poppets1;'
        r'UID=sa;'
        r'PWD=123456;'
    )
    conn = pyodbc.connect(conn_str)

    # Execute a consulta SQL para obter os dados do ano especificado
    query = f"SELECT idPieza, pPoppetpos, ts FROM poppet WHERE YEAR(ts) = {year}"
    data = pd.read_sql(query, conn)

    # Feche a conexão após a obtenção dos dados
    conn.close()

    # Converta a coluna 'ts' para datetime
    data['ts'] = pd.to_datetime(data['ts'])

    # Resample dos dados por mês para calcular a média mensal de pPoppetpos
    monthly_data = data.resample('M', on='ts')['pPoppetpos'].mean()

    # Crie o gráfico da série temporal
    plt.figure(figsize=(12, 6))  # Ajuste o tamanho da figura conforme necessário
    plt.plot(monthly_data.index, monthly_data.values, marker='o', linestyle='-')

    # Defina os rótulos e o título com uma reflexão precisa do eixo y
    plt.xlabel('Mês')
    plt.ylabel('Média de pPoppetpos')
    plt.title(f'Média de pPoppetpos por Mês em {year}')

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

@app.route('/graph/<int:year>')
def graph(year):
    graph = generate_plot(year)
    return render_template('graph.html', graph=graph)


if __name__ == "__main__":
    app.run(debug=True)