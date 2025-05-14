import pandas as pd
import kagglehub
from pathlib import Path
from pymongo import MongoClient

# --------------------
# ETAPA 1: EXTRACCIÓN
# --------------------

# Descargar el dataset de KaggleHub
path = Path(kagglehub.dataset_download("rodrack/medallistas-panamericanos-de-centroamrica"))

# Ruta del archivo CSV descargado
csv_file = path / "medallistas_panamericanos_CA.csv"

# Cargar el CSV en un DataFrame
df = pd.read_csv(csv_file)

# ---------------------
# ETAPA 2: TRANSFORMACIÓN
# ---------------------

# Revisión inicial
print("Columnas:", df.columns)
print("Primeras filas:")
print(df.head())

# Limpieza básica (ejemplo: eliminar filas nulas y columnas innecesarias)
df_clean = df.dropna()  # Quitar filas con valores nulos

# Opcional: convertir a diccionarios (documentos MongoDB)
records = df_clean.to_dict(orient="records")

# ---------------------
# ETAPA 3: CARGA EN MongoDB Atlas
# ---------------------

# URI de MongoDB Atlas
uri = "mongodb+srv://Countries:Country1@cluster0.0b8ol.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Conexión al cliente MongoDB
client = MongoClient(uri)

# Selección de base de datos y colección
db = client["Panamericanos"]
collection = db["Medallistas"]

# Cargar los datos
collection.delete_many({})  # Opcional: limpiar colección antes de insertar
collection.insert_many(records)

print(f"Se han insertado {len(records)} documentos en MongoDB Atlas.")

# Cierre de conexión
client.close()
