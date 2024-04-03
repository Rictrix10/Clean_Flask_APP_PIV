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