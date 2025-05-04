import pyautogui
import time

def get_mouse_position():
    """
    Muestra las coordenadas del puntero del ratón después de un tiempo de espera.
    Mueve el ratón a la ubicación deseada y presiona Enter para obtener las coordenadas.
    """
    print("Mueve el ratón a la ubicación deseada y presiona Enter")
    time.sleep(5)  # Espera 5 segundos

    # Obtener las coordenadas actuales del ratón
    x, y = pyautogui.position()
    print(f"Las coordenadas del ratón son: ({x}, {y})")

# Llamada a la función
get_mouse_position()
