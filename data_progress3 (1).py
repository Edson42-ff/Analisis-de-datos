import pandas as pd
from datetime import datetime


df = pd.read_csv(r'C:\Users\sefse\Downloads\pipol_dataset (1).csv')

df['birthday'] = pd.to_datetime(df['birthday'], format='%d/%m/%Y', errors='coerce')

fecha_actual = pd.to_datetime('today')
df['edad'] = (fecha_actual - df['birthday']).dt.days // 365.25

print("--- RESULTADOS DE LA ACTIVIDAD ---")


print("\na) Grupo: Mexico, Dusty City")
print("-" * 40)


grupo_pais_ciudad = df.groupby(['country', 'city'])


mexico_dusty = grupo_pais_ciudad.get_group(('Mexico', 'Dusty City'))
print(mexico_dusty[['name', 'last_name', 'country', 'city', 'edad']].head()) 

print("\nb) Edad promedio por país")
print("-" * 40)

edad_promedio_pais = df.groupby('country').agg({'edad': 'mean'})


edad_promedio_pais = edad_promedio_pais.rename(columns={'edad': 'edad_promedio'})


edad_promedio_pais = edad_promedio_pais.round(2)

print(edad_promedio_pais)