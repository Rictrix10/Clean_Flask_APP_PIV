import pandas as pd
import pyodbc

# Defina a string de conexão com os detalhes do seu servidor e banco de dados
conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=ASUSTUFGAMING\EI28235;'
    r'DATABASE=poppets1;'
    r'UID=sa;'
    r'PWD=123456;'
)

# Estabeleça a conexão
conn = pyodbc.connect(conn_str)

# Carregue os dados do arquivo CSV para um DataFrame
data = pd.read_csv('../csv/dadosPoppet.csv')

# Iterar sobre as linhas do DataFrame e inserir os dados na tabela 'poppet'
for index, row in data.iterrows():
    idPieza = row['idPieza']
    pPoppetpos = row['pPoppetpos']
    ts = row['Ts']
    
    # Formate os valores para a consulta SQL
    idPieza = int(idPieza)
    pPoppetpos = float(pPoppetpos)
    ts = pd.to_datetime(ts)  # Converta para datetime se necessário
    
    # Execute a consulta SQL para inserir os dados
    cursor = conn.cursor()
    cursor.execute("INSERT INTO poppet (idPieza, pPoppetpos, ts) VALUES (?, ?, ?)", idPieza, pPoppetpos, ts)
    conn.commit()
    cursor.close()

# Feche a conexão após a inserção dos dados
conn.close()
