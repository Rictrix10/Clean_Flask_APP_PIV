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

# Execute a consulta SQL para excluir os registros com pPoppetpos inferior a 1.0
cursor = conn.cursor()
cursor.execute("DELETE FROM poppet WHERE pPoppetpos < ?", 1.0)
conn.commit()
cursor.close()

# Feche a conexão após a exclusão dos dados
conn.close()

