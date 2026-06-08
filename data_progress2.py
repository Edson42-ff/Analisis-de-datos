import pandas as pd
import datetime

# Cargar dataset
df = pd.read_csv("pipol_dataset.csv")

# 1) Convertir birthday a tipo datetime
df['birthday'] = pd.to_datetime(df['birthday'])

print("=== DataFrame con birthday convertido a datetime ===")
print(df)

# Calcular edad aproximada (solo por año)
df['age'] = datetime.datetime.now().year - df['birthday'].dt.year

print("\n=== DataFrame con columna age agregada ===")
print(df.head())

# 2) Agrupar personas por ciudad
group_city = df.groupby("city")

print("\n=== Personas agrupadas por ciudad ===")
print(group_city.size())

# 3) Edad promedio por país
avg_age_country = df.groupby("country")["age"].mean()

print("\n=== Edad promedio por país ===")
print(avg_age_country)

# Otra forma usando agg()
avg_age_country2 = df.groupby("country").agg(promedio_edad=("age", "mean"))

print("\n=== Edad promedio por país usando agg() ===")
print(avg_age_country2)
