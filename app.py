import json
from flask import Flask, flash, redirect, render_template, request, jsonify, send_file, session, url_for
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from functions import generate_correlation_matrix
from functions import generate_corr_matrix_solders


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

def calculate_statistics(year):
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=ASUSTUFGAMING\EI28235;'
        r'DATABASE=poppets1;'
        r'UID=sa;'
        r'PWD=123456;'
    )
    conn = pyodbc.connect(conn_str)

    query = f"SELECT pPoppetpos FROM poppet WHERE YEAR(ts) = {year}"
    data = pd.read_sql(query, conn)

    conn.close()

    statistics = {
        'Minimo': round(data['pPoppetpos'].min(), 2),
        'Maximo': round(data['pPoppetpos'].max(), 2),
        'Media': round(data['pPoppetpos'].mean(), 2),
        'Mediana': round(data['pPoppetpos'].median(), 2),
        'Moda': round(data['pPoppetpos'].mode()[0], 2),
        'Desvio Padrao': round(data['pPoppetpos'].std(), 2),
        'Amplitude': round(data['pPoppetpos'].max() - data['pPoppetpos'].min(), 2)
    }

    return statistics



def generate_plot(year):
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=ASUSTUFGAMING\EI28235;'
        r'DATABASE=poppets1;'
        r'UID=sa;'
        r'PWD=123456;'
    )
    conn = pyodbc.connect(conn_str)

    query = f"SELECT idPieza, pPoppetpos, ts FROM poppet WHERE YEAR(ts) = {year}"
    data = pd.read_sql(query, conn)

    conn.close()

    data['ts'] = pd.to_datetime(data['ts'])
    monthly_data = data.resample('M', on='ts')['pPoppetpos'].mean()

    plt.figure(figsize=(6, 4)) 
    plt.plot(monthly_data.index.strftime('%b'), monthly_data.values, marker='o', linestyle='-') # Exibir apenas os meses no eixo x

    plt.xlabel('Mês')
    plt.ylabel('Média de pPoppetpos')
    plt.title(f'Média de pPoppetpos por Mês em {year}')

    plt.xticks(rotation=45)  

    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode()
    buffer.close()

    return graph

def generate_scatter_plot(year):
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=ASUSTUFGAMING\EI28235;'
        r'DATABASE=poppets1;'
        r'UID=sa;'
        r'PWD=123456;'
    )
    conn = pyodbc.connect(conn_str)

    query = f"SELECT pPoppetpos, ts FROM poppet WHERE YEAR(ts) = {year}"
    data = pd.read_sql(query, conn)

    conn.close()

    plt.figure(figsize=(6, 4)) 
    plt.scatter(data['ts'], data['pPoppetpos'], alpha=0.5)
    
    plt.xlabel('Timestamp')
    plt.ylabel('pPoppetpos')
    plt.title(f'Dispersão de pPoppetpos por Tempo em {year}')

    plt.xticks(rotation=45)  

    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode()
    buffer.close()

    return graph


app = Flask(__name__)
app.secret_key = 'secretkeysparepartscroston'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    current_year = request.args.get('year', default=2024, type=int)
    graph = generate_plot(current_year)
    return render_template('home.html', graph=graph, current_year=current_year)

@app.route('/graph/<int:year>')
def graph(year):
    graph = generate_plot(year)
    return render_template('graph.html', graph=graph)

@app.route('/statistics/<int:year>')
def get_statistics(year):
    statistics = calculate_statistics(year)
    return jsonify(statistics)

@app.route('/scatter_plot/<int:year>')
def scatter_plot(year):
    graph = generate_scatter_plot(year)
    return render_template('scatter_plot.html', graph=graph, year=year)

@app.route('/correlation_matrix')
def correlation_matrix():
    image_base64 = generate_correlation_matrix()
    return render_template('correlation_matrix.html', image_base64=image_base64)

@app.route('/correlation_matrix_solders')
def correlation_matrix_solders():
    image_base64 = generate_corr_matrix_solders()
    return render_template('correlation_matrix_solders.html', image_base64=image_base64)


if __name__ == "__main__":
    app.run(debug=True)
