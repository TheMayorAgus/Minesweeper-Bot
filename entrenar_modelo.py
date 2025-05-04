import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Función para cargar todas las celdas desde las subcarpetas
def cargar_todas_las_celdas(base_dir="celdas"):
    X, y = [], []
    for subcarpeta in os.listdir(base_dir):
        ruta_completa = os.path.join(base_dir, subcarpeta)
        if os.path.isdir(ruta_completa):
            for archivo in os.listdir(ruta_completa):
                if archivo.endswith(".png") and "_" in archivo:
                    ruta_imagen = os.path.join(ruta_completa, archivo)
                    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
                    if imagen is None:
                        continue
                    imagen_redimensionada = cv2.resize(imagen, (20, 20)).flatten()
                    X.append(imagen_redimensionada)
                    
                    # Extraer la clase de acuerdo al nombre del archivo
                    partes = archivo.split("_")
                    if len(partes) >= 4:
                        # Etiquetar según la palabra en el nombre del archivo
                        if "bomba" in partes[-1]:  # Si la imagen tiene "bomba" en el nombre
                            y.append(1)  # Bomba
                        elif "vacía" in partes[-1]:  # Si la imagen tiene "vacía" en el nombre
                            y.append(0)  # Celda vacía
                        else:
                            y.append(2)  # Número (por defecto, si no es bomba ni vacía)
    return np.array(X), np.array(y)

# Cargar todas las imágenes etiquetadas
X, y = cargar_todas_las_celdas()

# Verificar si hay datos para entrenar
if len(X) == 0 or len(y) == 0:
    raise ValueError("❌ No se encontraron datos para entrenar. Asegúrate de tener imágenes etiquetadas.")

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo
modelo = RandomForestClassifier(n_estimators=100)
modelo.fit(X_train, y_train)

# Evaluación del modelo
precision = modelo.score(X_test, y_test)
print(f"✅ Precisión en test: {precision:.2f}")

# Guardar el modelo entrenado
os.makedirs("modelo", exist_ok=True)
joblib.dump(modelo, "modelo/minas_modelo.pkl")
print("💾 Modelo guardado en 'modelo/minas_modelo.pkl'")
