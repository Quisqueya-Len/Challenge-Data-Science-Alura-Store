import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carga de datos
clientes = pd.read_csv("clientes.csv")
llamadas = pd.read_csv("llamadas.csv")
internet = pd.read_csv("internet.csv")

# Limpieza
clientes.drop_duplicates(inplace=True)
llamadas.drop_duplicates(inplace=True)
internet.drop_duplicates(inplace=True)

clientes.fillna({"genero":"Desconocido","dependientes":0,"servicio_telefonico":"No"}, inplace=True)
llamadas.fillna(0, inplace=True)
internet.fillna(0, inplace=True)

# Unificación
df = clientes.merge(llamadas, on="id_cliente", how="left")
df = df.merge(internet, on="id_cliente", how="left")

# Transformaciones
df["antiguedad_meses"] = df["antiguedad"].apply(lambda x: int(str(x).replace(" meses","")))
df["gasto_total"] = df["gasto_mensual"] * df["antiguedad_meses"]
df["churn"] = df["estado"].apply(lambda x: 1 if x=="Churn" else 0)

# KPIs
kpis = {
    "clientes_totales": df["id_cliente"].nunique(),
    "churn_rate": df["churn"].mean(),
    "ingresos_totales": df["gasto_total"].sum(),
    "ticket_promedio": df["gasto_mensual"].mean()
}

# Visualizaciones
plt.figure(figsize=(6,4))
sns.barplot(x=df["churn"].value_counts().index, y=df["churn"].value_counts().values)
plt.title("Clientes con y sin churn")
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df["gasto_mensual"], bins=30)
plt.title("Distribución de gasto mensual")
plt.show()

plt.figure(figsize=(6,4))
sns.boxplot(x="churn", y="gasto_mensual", data=df)
plt.title("Gasto mensual vs Churn")
plt.show()
