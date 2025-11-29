# 🐦 Birds & Planes

Un juego tipo Frogger donde controlas un pájaro que debe cruzar carriles esquivando aviones.

## 🎮 ¡JUGAR AHORA! (Versión Web)

### 👉 [CLICK AQUÍ PARA JUGAR](https://luisalfonso634.github.io/Birds-Planes/) 👈

No necesitas instalar nada. Funciona en cualquier navegador moderno.

---

## 🚀 INSTALACIÓN LOCAL (Opcional)

Si prefieres ejecutarlo en tu computadora:

### Requisitos
- **Python 3.8 o superior** - [Descargar](https://www.python.org/downloads/)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/luisalfonso634/Birds-Planes.git
cd Birds-Planes

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar sprites (solo la primera vez)
python generate_placeholders.py

# 4. Ejecutar
python main.py
```

---

## 🎮 CONTROLES

| Tecla | Acción |
|:-----:|--------|
| **ESPACIO** | Iniciar partida |
| **↑ ↓ ← →** | Mover el pájaro |
| **P** | Pausar / Reanudar |
| **M** | Sonido ON / OFF |
| **R** | Reiniciar (Game Over) |
| **ESC** | Menú / Salir |

---

## 🎯 CÓMO JUGAR

1. **Inicio**: Tu pájaro está en la zona verde (abajo)
2. **Meta**: Llegar a la zona azul "¡META!" (arriba)
3. **Obstáculos**: ¡Esquiva los aviones!
4. **Puntos**: +100 por carril cruzado, +200 bonus al llegar

### Vidas
- Empiezas con **3 vidas** ❤️❤️❤️
- Pierdes 1 vida al chocar
- **Game Over** = 0 vidas

---

## ⚙️ CONFIGURACIÓN

Edita `config.json` para personalizar:

```json
{
    "numLanes": 5,           // Carriles
    "lives": 3,              // Vidas
    "pointsPerCross": 100,   // Puntos por carril
    "spawnRate": 1.0,        // Frecuencia aviones
    "planeSpeedRange": [150, 320],  // Velocidad
    "birdSpeed": 200         // Velocidad pájaro
}
```

---

## 📁 ESTRUCTURA

```
Birds-Planes/
├── main.py                  # Código del juego
├── config.json              # Configuración
├── requirements.txt         # Dependencias
├── generate_placeholders.py # Generador de sprites
├── highscore.json          # Tu récord
├── assets/                 # Sprites
│   ├── bird_*.png          # Pájaro (3 frames)
│   ├── plane_*.png         # Aviones
│   └── background.png      # Fondo
└── .github/workflows/      # Deploy automático
```

---

## 🌐 DEPLOY WEB (GitHub Pages)

El juego se compila automáticamente a versión web cuando haces push a `main`.

### Activar GitHub Pages:
1. Ve a tu repo → **Settings** → **Pages**
2. En "Source" selecciona **GitHub Actions**
3. ¡Listo! El juego estará en `https://tu-usuario.github.io/Birds-Planes/`

### Compilar manualmente:
```bash
pip install pygbag
pygbag main.py
```

---

## 🔗 COMPARTIR EN REDES SOCIALES

Copia este enlace para compartir:
```
https://luisalfonso634.github.io/Birds-Planes/
```

Texto sugerido:
> 🎮 ¡Acabo de crear un juego! Ayuda al pájaro a esquivar los aviones. 
> ¿Puedes superar mi récord? 🐦✈️
> 👉 https://luisalfonso634.github.io/Birds-Planes/

---

## 📝 LICENCIA

MIT License - Libre para uso personal y comercial.

---

**¡Diviértete jugando! 🎮🐦✈️**
