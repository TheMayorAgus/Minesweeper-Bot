import os
import cv2
import numpy as np
import pyautogui
import time
import joblib
import random

# Coordenadas y configuración del tablero (ajustar según tu resolución de pantalla)
x, y = 1266, 323  # Coordenada superior izquierda del tablero
width, height = 466, 465  # Dimensiones del tablero
grid_size = 10  # Número de celdas por fila y columna

# Cargar el modelo de predicción (asegúrate de tener el modelo entrenado previamente)
modelo = joblib.load("modelo/minas_modelo.pkl")

# Cargar la plantilla de "Game Over" (asegúrate de tener esta imagen)
game_over_img = cv2.imread("game_over.png", cv2.IMREAD_GRAYSCALE)

# Conjunto para almacenar celdas ya clickeadas
celdas_clickeadas = set()

def capturar_tablero():
    """Captura la pantalla del área donde se encuentra el tablero."""
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    imagen = np.array(screenshot)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
    return imagen

def hacer_click(x_click, y_click):
    """Hace clic en las coordenadas especificadas."""
    print(f"Intentando hacer clic en: ({x_click}, {y_click})")  # Depuración de clic
    pyautogui.click(x_click, y_click)
    print(f"✅ Click realizado en: ({x_click}, {y_click})")

def juego_terminado(imagen_juego):
    """Detecta si el juego ha terminado buscando la imagen de 'Game Over'.""" 
    imagen_juego_gray = cv2.cvtColor(imagen_juego, cv2.COLOR_BGR2GRAY)

    # Redimensionar la imagen de 'Game Over' para que tenga un tamaño adecuado
    game_over_resized = cv2.resize(game_over_img, (imagen_juego_gray.shape[1], imagen_juego_gray.shape[0]))

    resultado = cv2.matchTemplate(imagen_juego_gray, game_over_resized, cv2.TM_CCOEFF_NORMED)
    umbral = 0.8  # Umbral de coincidencia
    loc = np.where(resultado >= umbral)

    if len(loc[0]) > 0:
        print("🛑 El juego ha terminado.")
        return True
    return False

def predecir_celda(imagen_celda):
    """Predice el valor de la celda (vacía, bomba, número)."""
    gris = cv2.cvtColor(imagen_celda, cv2.COLOR_BGR2GRAY)
    redim = cv2.resize(gris, (20, 20)).flatten().reshape(1, -1)
    start_time = time.time()
    pred = modelo.predict(redim)
    print(f"Tiempo de predicción: {time.time() - start_time} segundos")
    print(f"Predicción de celda: {pred[0]}")  # Depuración de predicción
    return pred[0]

def realizar_primer_clic():
    """Hace un clic en una celda aleatoria al inicio del juego."""
    col = random.randint(0, grid_size - 1)
    fila = random.randint(0, grid_size - 1)

    x_click = x + (col * (width // grid_size)) + (width // (2 * grid_size))
    y_click = y + (fila * (height // grid_size)) + (height // (2 * grid_size))

    hacer_click(x_click, y_click)

    # Añadir la celda clickeada al conjunto
    celdas_clickeadas.add((fila, col))

def main():
    """Función principal que ejecuta el bot de Buscaminas."""
    print("🟢 Iniciando bot automático de Buscaminas...")

    # Hacer el primer clic
    realizar_primer_clic()

    while True:
        # Capturar el tablero del juego
        imagen = capturar_tablero()

        # Mostrar imagen (opcional, solo para depuración)
        cv2.imshow("Tablero", imagen)

        # Verificar si el juego ha terminado
        if juego_terminado(imagen):
            print("🛑 El juego ha terminado, cerrando programa.")
            break

        # Recorrer las celdas para realizar clics
        for fila in range(grid_size):
            for col in range(grid_size):
                # Si ya se ha clickeado esta celda, la omitimos
                if (fila, col) in celdas_clickeadas:
                    continue

                # Calculamos las coordenadas de la celda a clicar
                x_click = x + (col * (width // grid_size)) + (width // (2 * grid_size))
                y_click = y + (fila * (height // grid_size)) + (height // (2 * grid_size))

                # Imprimir las coordenadas calculadas para depuración
                print(f"Coordenadas calculadas: ({x_click}, {y_click})")

                # Predicción de la celda (vacía, bomba, número)
                celda = imagen[fila * (height // grid_size):(fila + 1) * (height // grid_size),
                               col * (width // grid_size):(col + 1) * (width // grid_size)]
                clase = predecir_celda(celda)

                # Realizar clic solo si
