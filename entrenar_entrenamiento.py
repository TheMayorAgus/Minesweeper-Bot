import os
import cv2
import numpy as np
import joblib
import shutil

# Cargar el modelo previamente entrenado
modelo = joblib.load("modelo/minas_modelo.pkl")

# Carpeta con nuevas celdas sin etiqueta
entrada = "celdas_sin_etiquetar/"
salida = "celdas/"

os.makedirs(salida, exist_ok=True)

for nombre in os.listdir(entrada):
    if nombre.endswith(".png"):
        ruta = os.path.join(entrada, nombre)
        imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        imagen_redimensionada = cv2.resize(imagen, (20, 20)).flatten().reshape(1, -1)

        prediccion = modelo.predict(imagen_redimensionada)[0]
        nuevo_nombre = nombre.replace(".png", f"_{prediccion}.png")
        nueva_ruta = os.path.join(salida, nuevo_nombre)

        shutil.copy(ruta, nueva_ruta)  # Copia con nuevo nombre
        print(f"🔍 {nombre} → {nuevo_nombre}")

print("✅ Autoetiquetado completo.")
