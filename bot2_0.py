import cv2
import numpy as np
import pyautogui
import pickle
import time
import os
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

# Coordenadas del área del juego
x1, y1 = 1266, 323
x2, y2 = 1732, 788
filas, columnas = 10, 10

# Cálculo del tamaño de celdas
ancho_total = x2 - x1
alto_total = y2 - y1
ancho_celda = ancho_total // columnas
alto_celda = alto_total // filas

# Cargar modelo entrenado y escalador
with open("modelo/minas_modelo.pkl", "wb") as f:
    pickle.dump(modelo, f)

escalador = pickle.load(open("escalador.pkl", "rb"))

# Mantener historial para no repetir clics
historial_clics = set()

def capturar_celdas():
    captura = pyautogui.screenshot(region=(x1, y1, ancho_total, alto_total))
    captura = cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR)
    celdas = []
    for fila in range(filas):
        for col in range(columnas):
            x_inicio = col * ancho_celda
            y_inicio = fila * alto_celda
            celda_img = captura[y_inicio:y_inicio + alto_celda, x_inicio:x_inicio + ancho_celda]
            celdas.append(((fila, col), celda_img))
    return celdas

def predecir_celda(img):
    img_redim = cv2.resize(img, (46, 46)).flatten().astype(np.float32)
    img_escalada = escalador.transform([img_redim])
    pred = modelo.predict(img_escalada)[0]
    return pred

def hacer_clic(fila, col):
    if (fila, col) in historial_clics:
        return
    historial_clics.add((fila, col))
    x_click = x1 + col * ancho_celda + ancho_celda // 2
    y_click = y1 + fila * alto_celda + alto_celda // 2
    pyautogui.click(x_click, y_click)
    print(f"Clic en ({fila}, {col})")

def imprimir_tablero(tablero):
    print("Tablero predicho:")
    for fila in range(filas):
        linea = ""
        for col in range(columnas):
            linea += str(tablero[fila][col]) + " "
        print(linea)

def actualizar_modelo(celdas):
    X_nuevas = []
    y_nuevas = []
    for (coord, img) in celdas:
        img_redim = cv2.resize(img, (46, 46)).flatten().astype(np.float32)
        img_escalada = escalador.transform([img_redim])
        pred = modelo.predict(img_escalada)[0]
        X_nuevas.append(img_redim)
        y_nuevas.append(pred)
    if hasattr(modelo, "partial_fit"):
        X_nuevas, y_nuevas = shuffle(X_nuevas, y_nuevas)
        escalador.partial_fit(X_nuevas)
        modelo.partial_fit(escalador.transform(X_nuevas), y_nuevas)
        print("Modelo actualizado.")

def detectar_fin_juego(celdas):
    grises = [cv2.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))[0] for (_, img) in celdas]
    return all(g < 50 or g > 220 for g in grises)

def main():
    print("Iniciando bot en 3 segundos...")
    time.sleep(3)

    primer_clic = True
    while True:
        celdas = capturar_celdas()

        if detectar_fin_juego(celdas):
            print("Juego terminado. Reiniciá el tablero.")
            break

        tablero = [[0] * columnas for _ in range(filas)]
        for (fila, col), img in celdas:
            pred = predecir_celda(img)
            tablero[fila][col] = pred

        imprimir_tablero(tablero)

        for (fila, col), _ in celdas:
            if tablero[fila][col] == 0:
                hacer_clic(fila, col)
                if primer_clic:
                    time.sleep(1)
                    primer_clic = False
                break

        actualizar_modelo(celdas)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
