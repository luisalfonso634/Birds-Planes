# 🐦 Birds & Planes

Un juego tipo Frogger desarrollado en Python con Pygame. Controla un pájaro que debe cruzar carriles llenos de aviones sin ser golpeado.

![Birds & Planes](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Requisitos

- **Python**: 3.8 o superior
- **Sistema operativo**: Windows, macOS o Linux
- **Dependencias**: Pygame 2.5+

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/birds-and-planes.git
cd birds-and-planes
```

O descarga el ZIP y extráelo en una carpeta.

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Generar assets placeholder

Si no tienes sprites personalizados, genera los placeholders:

```bash
python generate_placeholders.py
```

Esto creará la carpeta `assets/` con los sprites necesarios.

## ▶️ Ejecutar el juego

```bash
python main.py
```

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| ↑ ↓ ← → | Mover el pájaro |
| P | Pausar / Reanudar |
| M | Activar / Desactivar sonido |
| R | Reiniciar (en Game Over) |
| ESC | Volver al menú / Salir |
| ESPACIO | Iniciar juego (en menú) |

## ⚙️ Configuración

Los parámetros del juego se pueden modificar en `config.json`:

```json
{
    "numLanes": 5,              // Número de carriles
    "lives": 3,                 // Vidas iniciales
    "pointsPerCross": 100,      // Puntos por cruzar un carril
    "spawnRate": 1.0,           // Aviones por segundo por carril (base)
    "planeSpeedRange": [150, 320], // Velocidad de aviones (px/s)
    "difficultyStepEveryXSeconds": 15, // Segundos entre incrementos de dificultad
    "difficultySpeedMultiplier": 1.08, // Multiplicador de velocidad por paso
    "minSpawnDistancePx": 120,  // Distancia mínima entre aviones
    "screenWidth": 800,         // Ancho de ventana
    "screenHeight": 600,        // Alto de ventana
    "birdSpeed": 200,           // Velocidad del pájaro
    "laneHeight": 80,           // Altura de cada carril
    "soundEnabled": true        // Sonido activado por defecto
}
```

### Parámetros explicados

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `numLanes` | Cantidad de carriles con aviones | 5 |
| `lives` | Vidas iniciales del jugador | 3 |
| `pointsPerCross` | Puntos al cruzar un carril | 100 |
| `spawnRate` | Frecuencia base de spawn de aviones | 1.0 |
| `planeSpeedRange` | Rango de velocidad de aviones [min, max] | [150, 320] |
| `difficultyStepEveryXSeconds` | Cada cuántos segundos aumenta la dificultad | 15 |
| `difficultySpeedMultiplier` | Factor de incremento de velocidad | 1.08 |
| `minSpawnDistancePx` | Espacio mínimo entre aviones para evitar overlap | 120 |

## 📁 Estructura del proyecto

```
birds-and-planes/
├── main.py                  # Código principal del juego
├── config.json              # Configuración del juego
├── requirements.txt         # Dependencias
├── highscore.json           # Récord (generado automáticamente)
├── generate_placeholders.py # Generador de sprites placeholder
├── README.md                # Este archivo
├── tests_manual.md          # Pruebas manuales
└── assets/                  # Sprites (generados o personalizados)
    ├── bird_1.png
    ├── bird_2.png
    ├── bird_3.png
    ├── plane_small.png
    ├── plane_med.png
    ├── plane_large.png
    └── background.png
```

## 🎨 Personalizar assets

Para usar tus propios sprites:

1. Crea imágenes PNG con fondo transparente
2. Reemplaza los archivos en `assets/`:
   - `bird_1.png`, `bird_2.png`, `bird_3.png` - Frames de animación del pájaro (32x32 px recomendado)
   - `plane_small.png` - Avión pequeño (48x24 px)
   - `plane_med.png` - Avión mediano (64x32 px)
   - `plane_large.png` - Avión grande (80x40 px)
   - `background.png` - Fondo del juego (800x600 px o tamaño de pantalla)

Si no se encuentran los archivos, el juego usa placeholders dibujados proceduralmente.

## 🔧 Mecánicas del juego

### Objetivo
Llevar al pájaro desde la zona segura (abajo) hasta la meta (arriba), cruzando todos los carriles sin chocar con aviones.

### Puntuación
- +100 puntos por cada carril cruzado
- +200 puntos (bonus) al llegar a la meta
- El récord se guarda automáticamente en `highscore.json`

### Vidas
- Empiezas con 3 vidas
- Pierdes 1 vida al chocar con un avión
- Al perder todas las vidas: Game Over

### Dificultad progresiva
- Cada 15 segundos, la velocidad de los aviones aumenta un 8%
- Los aviones pequeños son más frecuentes pero más rápidos
- Los aviones grandes son más lentos pero ocupan más espacio

## 📦 Empaquetar para distribución

### Crear archivo ZIP

```bash
# Windows (PowerShell)
Compress-Archive -Path main.py, config.json, requirements.txt, generate_placeholders.py, README.md, tests_manual.md, assets -DestinationPath birds-and-planes.zip

# Linux/macOS
zip -r birds-and-planes.zip main.py config.json requirements.txt generate_placeholders.py README.md tests_manual.md assets/
```

### Crear ejecutable con PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "config.json;." main.py
```

El ejecutable estará en `dist/main.exe` (Windows) o `dist/main` (Linux/macOS).

## 🌐 Exportar a Web (HTML5)

El juego está hecho en Pygame, que no tiene soporte nativo para web. Opciones:

### Opción 1: Pygbag (recomendado)

```bash
pip install pygbag
pygbag main.py
```

Esto genera una versión web compatible con navegadores modernos.

### Opción 2: Reescribir en JavaScript

Para una versión web nativa, considera portar el juego a:
- **Phaser.js** - Framework de juegos HTML5
- **PixiJS** - Motor de renderizado 2D
- **Kaboom.js** - Framework simple para juegos

## 💼 Integrar en Microsoft Teams

Para usar el juego en Teams como una pestaña/app:

1. **Exportar a HTML5** usando Pygbag
2. **Hospedar** los archivos en un servidor web (Azure, GitHub Pages, etc.)
3. **Crear una app de Teams**:
   - Usar Teams App Studio o Teams Toolkit
   - Configurar como "Tab app" con la URL del juego
4. **Publicar** la app en tu organización

Consulta la [documentación de Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/tabs/what-are-tabs) para más detalles.

## 🐛 Solución de problemas

### El juego no inicia

1. Verifica que Python esté instalado: `python --version`
2. Verifica que Pygame esté instalado: `pip show pygame`
3. Genera los assets: `python generate_placeholders.py`

### No hay sonido

- Algunos sistemas no soportan el mixer de Pygame
- El juego funciona sin sonido (muestra advertencia en consola)
- Presiona M para activar/desactivar sonido

### Los assets no cargan

- Ejecuta `python generate_placeholders.py` para crearlos
- Verifica que la carpeta `assets/` exista

### El highscore no se guarda

- Verifica permisos de escritura en la carpeta del juego
- El archivo `highscore.json` debe poder crearse/modificarse

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Créditos

- Desarrollado con Python y Pygame
- Sprites placeholder generados proceduralmente
- Diseño inspirado en Frogger (Konami, 1981)

---

**¡Diviértete jugando Birds & Planes! 🎮**

