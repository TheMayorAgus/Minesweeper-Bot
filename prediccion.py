import os
import cv2
import numpy as np
import joblib

modelo = joblib.load("modelo/minas_modelo.pkl")

def predecir_celda(imagen_celda):
    gris = cv2.cvtColor(imagen_celda, cv2.COLOR_BGR2GRAY)
    redim = cv2.resize(gris, (20, 20)).flatten().reshape(1, -1)
    pred = modelo.predict(redim)
    return pred[0]

# Ejemplo
for nombre in os.listdir("celdas"):
    if nombre.endswith(".png"):
        ruta = os.path.join("celdas", nombre)
        imagen = cv2.imread(ruta)
        clase = predecir_celda(imagen)
        print(f"{nombre}: {clase}")
