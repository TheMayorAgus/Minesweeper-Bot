import cv2

def obtener_coordenadas(event, x, y, flags, param):
    """
    Función de callback para obtener las coordenadas del clic.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas del clic: ({x}, {y})")

def get_click_coordinates(image_path):
    """
    Muestra una imagen en una ventana de OpenCV y captura las coordenadas de los clics.
    """
    cv2.namedWindow("Haz clic en la ubicación deseada")
    cv2.setMouseCallback("Haz clic en la ubicación deseada", obtener_coordenadas)

    while True:
        img = cv2.imread(image_path)  # Cargar la imagen (puedes usar una captura del juego)
        cv2.imshow("Haz clic en la ubicación deseada", img)
        
        # Presionar 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Llamada a la función
get_click_coordinates('C:\Users\Outlet VL\OneDrive\Documentos\Python Codes\Bot_juego\clicks\captura_tablero.png')  # Reemplaza con la ruta de tu imagen
