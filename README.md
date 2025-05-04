
# 🤖 Bot de Buscaminas Automatizado (con IA y Visión por Computadora)

Este proyecto busca automatizar el juego de Buscaminas usando visión por computadora y un modelo de machine learning. El sistema detecta las celdas del tablero, predice su contenido (vacía, número o mina), y actúa en consecuencia.

---

## 📁 Estructura de Carpetas

```
.
├── bot_jugador.py              # Ejecuta el bot y hace clics automáticamente
├── captura_tablero.py         # Captura screenshots del juego mientras se juega manualmente
├── entrenar_modelo.py         # Entrena el modelo a partir de las imágenes etiquetadas
├── entrenar_entrenamiento.py  # Etiqueta automáticamente las imágenes sin clasificar
├── get_mouse_position.py      # Utilidad para obtener las coordenadas del tablero
├── escalador.py               # (En desarrollo) Sistema de mejora progresiva del modelo
├── bot2_0.py                  # (En desarrollo) Automatización completa con autoentrenamiento
├── modelo/
│   └── minas_modelo.pkl       # Archivo del modelo entrenado
├── celdas/
│   ├── juego_1/
│   ├── juego_2/
│   └── ...                    # Imágenes etiquetadas manualmente (nombre: celda_x_y_etiqueta.png)
├── celdas_sin_etiquetar/      # Imágenes capturadas sin etiquetar
├── capturas/                  # Capturas completas del tablero
├── game_over.png              # Imagen para detectar fin del juego
└── README.md
```

---

## 🚀 ¿Cómo empezar?

### 1. Obtener coordenadas del tablero

Ejecutá:

```bash
python get_mouse_position.py
```

Esto imprimirá la posición de tu mouse cada medio segundo. Posicionate sobre el extremo superior izquierdo del tablero y anotá las coordenadas `x, y`.

### 2. Capturar datos manualmente

Jugá partidas mientras ejecutás:

```bash
python captura_tablero.py
```

Esto generará imágenes de celdas (`celda_x_y.png`) en una carpeta nueva dentro de `celdas/juego_n/`. 

### 3. Etiquetar imágenes automáticamente

Si ya tenés un modelo previamente entrenado, podés etiquetar automáticamente las celdas sin clasificar:

```bash
python entrenar_entrenamiento.py
```

Esto moverá y renombrará las celdas según su predicción (`celda_x_y_0.png`, etc.) y las dejará listas para nuevo entrenamiento.

### 4. Entrenar el modelo

Asegurate de tener varias carpetas (`juego_1`, `juego_2`, etc.) con imágenes de celdas bien clasificadas.

Luego, corré:

```bash
python entrenar_modelo.py
```

Esto generará `modelo/minas_modelo.pkl`.

### 5. Ejecutar el bot

Configurá el `bot_jugador.py` con las coordenadas correctas (`x`, `y`, `width`, `height`, `grid_size`) y luego corré:

```bash
python bot_jugador.py
```

---

## 🧠 Clases del modelo

- `0`: Celda vacía 
- `1`: Mina 
- `2`: Número 

---

## ⚠️ Limitaciones conocidas

- El bot no hace el primer clic automáticamente (por ahora).
- El sistema de detección de "Game Over" puede no funcionar según resolución o calidad del `game_over.png`.
- Las predicciones a veces no son confiables si no hay suficientes ejemplos bien etiquetados.
- El `escalador.py` y `bot2_0.py` están en desarrollo.

---

## ✅ Próximos pasos

- [ ] Agregar lógica para que el primer clic sea aleatorio y seguro.
- [ ] Mejorar detección del fin del juego con OCR o cambios de color.
- [ ] Implementar autoentrenamiento (escalador.py).
- [ ] Reforzar el entrenamiento con imágenes de diferentes resoluciones y estilos visuales.
