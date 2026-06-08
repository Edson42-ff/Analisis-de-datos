import sqlite3
import pandas as pd

print("Iniciando fase LOAD del proceso ETL...")

# 1. Leer el archivo CSV
df = pd.read_csv('members.csv')

# 2. Conectar a la base de datos 
conn = sqlite3.connect('database_eiaa.db')

# 3. Cargar los datos en la tabla 'miembros'
df.to_sql('miembros', conn, if_exists='replace', index=False)

# 4. Cerrar la conexión
conn.close()

print("¡Proceso completado! La base de datos 'database_eiaa.db' se guardó exitosamente.")