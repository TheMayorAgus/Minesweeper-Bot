import cv2
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Cargar las imágenes de celdas
def cargar_celdas(carpeta):
    celdas = []
    etiquetas = []
    
    # Itera sobre las subcarpetas dentro de la carpeta principal 'celdas'
    for idx, carpeta_etiqueta in enumerate(os.listdir(carpeta)):
        carpeta_etiqueta_path = os.path.join(carpeta, carpeta_etiqueta)
        
        if os.path.isdir(carpeta_etiqueta_path):  # Verifica si es una subcarpeta
            for imagen_nombre in os.listdir(carpeta_etiqueta_path):
                imagen_path = os.path.join(carpeta_etiqueta_path, imagen_nombre)
                imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
                imagen = cv2.resize(imagen, (46, 46)).flatten()  # Redimensionar a 46x46 píxeles
                celdas.append(imagen)
                etiquetas.append(idx)  # Usar el índice de la carpeta como etiqueta
    
    return np.array(celdas), np.array(etiquetas)

# Ruta de la carpeta donde están las imágenes de celdas
carpeta_celdas = 'celdas'  # Asegúrate de que esta sea la ruta correcta

# Cargar y preparar datos
X, y = cargar_celdas(carpeta_celdas)

# Normalización con StandardScaler
escalador = StandardScaler()
X_escalado = escalador.fit_transform(X)

# Entrenamiento del modelo
modelo = RandomForestClassifier(n_estimators=100)
modelo.fit(X_escalado, y)

# Guardar el modelo y el escalador
with open('modelo.pkl', 'wb') as f:
    pickle.dump(modelo, f)
with open('escalador.pkl', 'wb') as f:
    pickle.dump(escalador, f)

print("Modelo y escalador entrenados y guardados.")
