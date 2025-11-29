# 🐦 Birds & Planes

Un juego tipo Frogger donde controlas un pájaro que debe cruzar carriles esquivando aviones.

---

## 🚀 INSTALACIÓN Y EJECUCIÓN RÁPIDA

### Requisitos previos
- **Python 3.8 o superior** - [Descargar aquí](https://www.python.org/downloads/)

### Pasos para ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/luisalfonso634/Birds-Planes.git
cd Birds-Planes

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar los sprites del juego (solo la primera vez)
python generate_placeholders.py

# 4. ¡Ejecutar el juego!
python main.py
```

---

## 🎮 CONTROLES

| Tecla | Acción |
|:-----:|--------|
| **ESPACIO** | Iniciar partida (en menú) |
| **↑** | Mover arriba |
| **↓** | Mover abajo |
| **←** | Mover izquierda |
| **→** | Mover derecha |
| **P** | Pausar / Reanudar |
| **M** | Sonido ON / OFF |
| **R** | Reiniciar (en Game Over) |
| **ESC** | Volver al menú / Salir |

---

## 🎯 OBJETIVO DEL JUEGO

1. **Inicio**: Tu pájaro comienza en la zona verde (abajo)
2. **Meta**: Llegar a la zona azul "¡META!" (arriba)
3. **Obstáculos**: Esquiva los aviones que cruzan en cada carril
4. **Puntuación**: +100 puntos por cada carril cruzado, +200 bonus al llegar a la meta

### Vidas
- Empiezas con **3 vidas** ❤️❤️❤️
- Pierdes 1 vida al chocar con un avión
- **Game Over** cuando pierdes todas las vidas

### Dificultad
- Cada 15 segundos los aviones se vuelven más rápidos (+8%)
- ¡Intenta superar tu récord!

---

## ⚙️ CONFIGURACIÓN

Edita el archivo `config.json` para personalizar el juego:

```json
{
    "numLanes": 5,           // Cantidad de carriles
    "lives": 3,              // Vidas iniciales
    "pointsPerCross": 100,   // Puntos por carril
    "spawnRate": 1.0,        // Frecuencia de aviones
    "planeSpeedRange": [150, 320],  // Velocidad min/max
    "difficultyStepEveryXSeconds": 15,  // Incremento cada X segundos
    "difficultySpeedMultiplier": 1.08,  // Factor de incremento
    "birdSpeed": 200,        // Velocidad del pájaro
    "soundEnabled": true     // Sonido activado
}
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
Birds-Planes/
├── main.py                  # Código principal del juego
├── config.json              # Configuración del juego
├── requirements.txt         # Dependencias (pygame)
├── generate_placeholders.py # Generador de sprites
├── highscore.json          # Tu récord (se genera automático)
├── README.md               # Este archivo
├── tests_manual.md         # Pruebas del juego
└── assets/                 # Sprites del juego
    ├── bird_1.png          # Pájaro frame 1
    ├── bird_2.png          # Pájaro frame 2
    ├── bird_3.png          # Pájaro frame 3
    ├── plane_small.png     # Avión pequeño
    ├── plane_med.png       # Avión mediano
    ├── plane_large.png     # Avión grande
    └── background.png      # Fondo del juego
```

---

## 🎨 PERSONALIZAR SPRITES

Para usar tus propios gráficos:

1. Crea imágenes PNG con fondo transparente
2. Reemplaza los archivos en `assets/`:

| Archivo | Tamaño recomendado |
|---------|-------------------|
| `bird_1.png`, `bird_2.png`, `bird_3.png` | 32x32 px |
| `plane_small.png` | 48x24 px |
| `plane_med.png` | 64x32 px |
| `plane_large.png` | 80x40 px |
| `background.png` | 800x600 px |

---

## ❓ SOLUCIÓN DE PROBLEMAS

### "No module named pygame"
```bash
pip install pygame
```

### "No se encuentran los assets"
```bash
python generate_placeholders.py
```

### El juego no abre ventana
- Verifica que tienes Python 3.8+: `python --version`
- Verifica pygame: `pip show pygame`

### No hay sonido
- Es normal en algunos sistemas
- Presiona **M** para verificar si está activado

---

## 📦 CREAR EJECUTABLE (.exe)

Para crear un ejecutable sin necesidad de Python:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "config.json;." main.py
```

El ejecutable estará en `dist/main.exe`

---

## 📝 LICENCIA

MIT License - Libre para uso personal y comercial.

---

**¡Diviértete jugando! 🎮🐦✈️**
