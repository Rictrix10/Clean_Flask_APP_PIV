import json
from flask import Flask, flash, redirect, render_template, request, jsonify, send_file, session, url_for
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from functions import generate_correlation_matrix
from functions import generate_corr_matrix_solders
from functions import select_corr_matrix_solder, generate_scatter_plot, generate_plot, calculate_statistics


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

@app.route('/graphics')
def graphics():
    return render_template('graphics.html')

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

'''
@app.route('/correlation_matrix')
def correlation_matrix():
    image_base64 = generate_correlation_matrix()
    return render_template('correlation_matrix.html', image_base64=image_base64)
'''

@app.route('/correlation_matrix')
def correlation_matrix_solder():
    image_base64 = select_corr_matrix_solder()
    return render_template('correlation_matrix.html', image_base64=image_base64)

'''
@app.route('/correlation_matrix_solders')
def correlation_matrix_solders():
    image_base64 = generate_corr_matrix_solders()
    return render_template('correlation_matrix_solders.html', image_base64=image_base64)
'''


if __name__ == "__main__":
    app.run(debug=True)
