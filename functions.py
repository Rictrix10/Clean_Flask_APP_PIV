import json
from flask import Flask, flash, redirect, render_template, request, jsonify, send_file, session, url_for
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns



def generate_correlation_matrix():
    df = pd.read_csv('./csv/dados_por_tratar.csv')
    correlation_matrix = df[['tensao_media_solda1 (Ueff/mV)','tensao_pico_solda1 (Umax/mV)','corrente_media_solda1 ','tempo_solda1 (time/ms)','energia_solda1 (J)','profundidade_solda1 (Depth/?m)','prof_fecho_solda1 (Closing Depth/?m)','tensao_media_solda2 (Ueff/mV)','tensao_pico_solda2 (Umax/mV)','corrente_media_solda2','tempo_solda2 (time/ms)','energia_solda2 (J)','profundidade_solda2 (Depth/?m)','prof_fecho_solda2 (Closing Depth/?m)','tensao_media_solda3 (Ueff/mV)','tensao_pico_solda3 (Umax/mV)','corrente_media_solda3','tempo_solda3 (time/ms)','energia_solda3 (J)','profundidade_solda3 (Depth/?m)','prof_fecho_solda3 (Closing Depth/?m)','resultado']].corr()

    # Plotar o heatmap
    plt.figure(figsize=(11, 11))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Heatmap')
    #plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    correlation_matrix = base64.b64encode(image_png).decode()
    buffer.close()

    return correlation_matrix

def generate_corr_matrix_solders():

    df = pd.read_csv('./csv/dados_por_tratar.csv')
    correlation_matrix = df[['tensao_media_solda1 (Ueff/mV)','tensao_pico_solda1 (Umax/mV)','corrente_media_solda1 ','tempo_solda1 (time/ms)','energia_solda1 (J)','profundidade_solda1 (Depth/?m)','prof_fecho_solda1 (Closing Depth/?m)','tensao_media_solda2 (Ueff/mV)','tensao_pico_solda2 (Umax/mV)','corrente_media_solda2','tempo_solda2 (time/ms)','energia_solda2 (J)','profundidade_solda2 (Depth/?m)','prof_fecho_solda2 (Closing Depth/?m)','tensao_media_solda3 (Ueff/mV)','tensao_pico_solda3 (Umax/mV)','corrente_media_solda3','tempo_solda3 (time/ms)','energia_solda3 (J)','profundidade_solda3 (Depth/?m)','prof_fecho_solda3 (Closing Depth/?m)','resultado']].corr()

    # Dividir a matriz de correlação em três partes correspondentes a cada solda
    solda1_corr = correlation_matrix.iloc[:7, :7]
    solda2_corr = correlation_matrix.iloc[7:14, 7:14]
    solda3_corr = correlation_matrix.iloc[14:-1, 14:-1]

    # Plotar os heatmaps para cada solda
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Heatmap para a solda 1
    sns.heatmap(solda1_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=axes[0])
    axes[0].set_title('Solda 1')

    # Heatmap para a solda 2
    sns.heatmap(solda2_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=axes[1])
    axes[1].set_title('Solda 2')

    # Heatmap para a solda 3
    sns.heatmap(solda3_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=axes[2])
    axes[2].set_title('Solda 3')

    plt.tight_layout()
    #plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    corr_matrix_solders = base64.b64encode(image_png).decode()
    buffer.close()

    return corr_matrix_solders

#def select_corr_matrix_solder(solder):
def select_corr_matrix_solder():
    df = pd.read_csv('./csv/dados_por_tratar.csv')
    correlation_matrix = df[['tensao_media_solda1 (Ueff/mV)','tensao_pico_solda1 (Umax/mV)','corrente_media_solda1 ','tempo_solda1 (time/ms)','energia_solda1 (J)','profundidade_solda1 (Depth/?m)','prof_fecho_solda1 (Closing Depth/?m)','tensao_media_solda2 (Ueff/mV)','tensao_pico_solda2 (Umax/mV)','corrente_media_solda2','tempo_solda2 (time/ms)','energia_solda2 (J)','profundidade_solda2 (Depth/?m)','prof_fecho_solda2 (Closing Depth/?m)','tensao_media_solda3 (Ueff/mV)','tensao_pico_solda3 (Umax/mV)','corrente_media_solda3','tempo_solda3 (time/ms)','energia_solda3 (J)','profundidade_solda3 (Depth/?m)','prof_fecho_solda3 (Closing Depth/?m)','resultado']].corr()

    # Dividir a matriz de correlação em três partes correspondentes a cada solda
    solda1_corr = correlation_matrix.iloc[:7, :7]
    solda2_corr = correlation_matrix.iloc[7:14, 7:14]
    solda3_corr = correlation_matrix.iloc[14:-1, 14:-1]

    # Plotar os heatmaps para cada solda
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Labels das colunas para cada solda
    col_labels = ['tensao_media', 'tensao_pico', 'corrente_media', 'tempo', 'energia', 'profundidade', 'prof_fecho']
    col_labels = ['ts', 'tp', 'cm', 't', 'e', 'p', 'pf']

    for i, solda_corr in enumerate([solda1_corr, solda2_corr, solda3_corr]):
        sns.heatmap(solda_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=axes[i], xticklabels=col_labels, yticklabels=col_labels, cbar=False)
        axes[i].set_title(f'Solda {i + 1}')

    plt.tight_layout()

    cbar = fig.colorbar(axes[-1].collections[0], ax=axes.ravel().tolist(), pad=0.04)
    #cbar.set_label('Correlation', rotation=270)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    corr_matrix_solders = base64.b64encode(image_png).decode()
    buffer.close()

    return corr_matrix_solders

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
    
    plt.xlabel('Timestamp (Month)')
    plt.ylabel('pPoppetpos')
    plt.title(f'Dispersão de pPoppetpos por Tempo em {year}')

    # Define o formato de data apenas para exibir os meses
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m'))

    plt.xticks(rotation=45)  

    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode()
    buffer.close()

    return graph

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


