import pyautogui
import cv2
import numpy as np
import time
import os

# --------------------------------------------
# CONFIGURACIÓN DEL ÁREA DEL JUEGO
# --------------------------------------------
x = 1033
y = 234
width = 683
height = 678
grid_size = 20

# --------------------------------------------
# Crea una carpeta de juego nueva automáticamente
# --------------------------------------------
def crear_nueva_carpeta(base="juego_", carpeta_padre="capturas"):
    i = 1
    while os.path.exists(os.path.join(carpeta_padre, f"{base}{i}")):
        i += 1
    nueva = os.path.join(carpeta_padre, f"{base}{i}")
    os.makedirs(nueva)
    return nueva

# --------------------------------------------
# Captura el tablero
# --------------------------------------------
def capturar_tablero():
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    imagen = np.array(screenshot)
    return cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)

# --------------------------------------------
# Divide imagen en celdas y las guarda
# --------------------------------------------
def dividir_en_celdas(imagen, carpeta_salida, grilla=10):
    alto_celda = imagen.shape[0] // grilla
    ancho_celda = imagen.shape[1] // grilla

    for fila in range(grilla):
        for col in range(grilla):
            y1 = fila * alto_celda
            y2 = (fila + 1) * alto_celda
            x1 = col * ancho_celda
            x2 = (col + 1) * ancho_celda
            celda = imagen[y1:y2, x1:x2]
            nombre = f"celda_{fila}_{col}.png"
            cv2.imwrite(os.path.join(carpeta_salida, nombre), celda)

# --------------------------------------------
# Hace clic en una coordenada
# --------------------------------------------
def hacer_click(x_click, y_click):
    pyautogui.click(x_click, y_click)
    print(f"✅ Click en: ({1372}, {605})")

# --------------------------------------------
# Bucle principal
# --------------------------------------------
def main():
    carpeta_juego = crear_nueva_carpeta()
    carpeta_celdas = carpeta_juego.replace("capturas", "celdas")
    os.makedirs(carpeta_celdas, exist_ok=True)

    ciclos_maximos = 50
    print(f"🟢 Iniciando bot... presiona 'q' para salir")

    for ciclo in range(ciclos_maximos):
        imagen = capturar_tablero()
        cv2.imshow("Tablero Buscaminas", imagen)

        timestamp = int(time.time())
        cv2.imwrite(os.path.join(carpeta_juego, f"captura_{timestamp}.png"), imagen)
        dividir_en_celdas(imagen, carpeta_celdas, grilla=grid_size)

        # Click ejemplo
        centro_x = x + width // 2
        centro_y = y + height // 2
        hacer_click(centro_x, centro_y)

        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Saliendo...")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
