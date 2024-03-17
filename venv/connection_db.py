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
