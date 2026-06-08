import pandas as pd
import sqlite3
from datetime import datetime


# Leer archivo CSV
df = pd.read_csv("members.csv")

print("DATASET ORIGINAL")
print(df.head())


# 1. Extraer código postal desde address
def extraer_codigo_postal(df, origen, destino):

    # Busca 5 números consecutivos
    df[destino] = df[origen].str.extract(r'(\d{5})')

    return df


# 2. Limpiar números telefónicos
def limpiar_telefono(df, columna):

    # Elimina +, (, ), -
    df[columna] = df[columna].str.replace(
        r'[\+\(\)\-]',
        '',
        regex=True
    )

    return df


# 3. Formatear fecha de nacimiento
def formatear_fecha(df, columna):

    # Convertir a fecha
    df[columna] = pd.to_datetime(
        df[columna],
        errors='coerce'
    )

    # Crear nueva columna con formato dia/mes/año
    df["fecha_formateada"] = df[columna].dt.strftime('%d/%m/%Y')

    return df


# 4. Calcular edad
def calcular_edad(df, columna):

    hoy = datetime.now()

    df["edad"] = df[columna].apply(
        lambda x:
        hoy.year - x.year -
        ((hoy.month, hoy.day) < (x.month, x.day))
        if pd.notnull(x)
        else None
    )

    return df


# Aplicar transformaciones
df = extraer_codigo_postal(df, "address", "codigo_postal")

df = limpiar_telefono(df, "phone_number")

df = formatear_fecha(df, "birth_date")

df = calcular_edad(df, "birth_date")


# Conectar a SQLite
conexion = sqlite3.connect("members.db")

# Guardar tabla
df.to_sql(
    "members",
    conexion,
    if_exists="replace",
    index=False
)

conexion.close()


print("\nDATASET TRANSFORMADO")
print(df.head())

print("\nProceso ETL completado correctamente.")