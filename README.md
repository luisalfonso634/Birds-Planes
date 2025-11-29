# 🐦 Birds & Planes

Un juego estilo Frogger donde controlas un pájaro que debe cruzar carriles esquivando aviones.

---

## 🎮 ¡JUGAR AHORA!

### 👉 [CLICK AQUÍ PARA JUGAR](https://luisalfonso634.github.io/Birds-Planes/) 👈

**Funciona en PC y celulares** - No necesitas instalar nada.

---

## 📱 Controles

### En PC (teclado):
| Tecla | Acción |
|:-----:|--------|
| **ESPACIO** | Iniciar |
| **↑ ↓ ← →** | Mover |
| **P** | Pausar |
| **R** | Reiniciar |

### En Móvil (táctil):
- **D-Pad virtual** en esquina inferior izquierda
- **Toca la pantalla** para iniciar/reiniciar

---

## 🎯 Cómo jugar

1. 🟢 **Inicio**: Tu pájaro está en la zona verde (abajo)
2. 🔵 **Meta**: Llega a la zona azul "META" (arriba)
3. ✈️ **Obstáculos**: ¡Esquiva los aviones!
4. ⭐ **Puntos**: +100 por carril, +200 bonus en la meta

### Vidas: ❤️❤️❤️
- 3 vidas iniciales
- Pierdes 1 al chocar
- Game Over = 0 vidas

---

## 💻 Ejecutar localmente

```bash
# Clonar
git clone https://github.com/luisalfonso634/Birds-Planes.git
cd Birds-Planes

# Instalar
pip install pygame

# Generar sprites
python generate_placeholders.py

# Jugar
python main.py
```

---

## ⚙️ Configuración

Edita `config.json`:

```json
{
    "numLanes": 5,
    "lives": 3,
    "pointsPerCross": 100,
    "birdSpeed": 200
}
```

---

## 📁 Estructura

```
Birds-Planes/
├── main.py          # Código del juego
├── config.json      # Configuración
├── assets/          # Sprites
├── docs/            # Versión web (GitHub Pages)
└── README.md
```

---

## 🔗 Compartir

```
https://luisalfonso634.github.io/Birds-Planes/
```

---

**Hecho con Python + Pygame 🐍🎮**
