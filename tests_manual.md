# 🧪 Pruebas Manuales - Birds & Planes

Este documento describe las pruebas manuales para verificar el correcto funcionamiento del juego.

## Pre-requisitos

1. Tener Python 3.8+ instalado
2. Tener Pygame instalado (`pip install pygame`)
3. Haber generado los assets (`python generate_placeholders.py`)
4. Poder ejecutar el juego (`python main.py`)

---

## Prueba 1: Colisión resta vida

### Objetivo
Verificar que al chocar con un avión, el jugador pierde una vida.

### Pasos
1. Iniciar el juego (`python main.py`)
2. Presionar ESPACIO para comenzar
3. Mover el pájaro hacia arriba (↑) hasta un carril con aviones
4. Dejar que un avión golpee al pájaro

### Resultado esperado
- ✅ El contador de vidas disminuye de 3 a 2
- ✅ El pájaro regresa a la posición inicial (zona segura)
- ✅ Se reproduce un sonido de colisión (si el sonido está activado)
- ✅ El juego continúa si quedan vidas

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 2: Cruce de carril suma puntos

### Objetivo
Verificar que cruzar un carril otorga puntos al jugador.

### Pasos
1. Iniciar el juego y comenzar partida
2. Observar la puntuación inicial (0)
3. Mover el pájaro hacia arriba atravesando un carril completo
4. Observar la puntuación después de cruzar

### Resultado esperado
- ✅ La puntuación aumenta en 100 puntos por cada carril cruzado
- ✅ Se reproduce un sonido de punto (si está activado)
- ✅ Al llegar a la meta, se reciben 200 puntos bonus
- ✅ El pájaro regresa a la zona segura al completar el cruce

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 3: Sistema de vidas y Game Over

### Objetivo
Verificar que el juego termina correctamente al perder todas las vidas.

### Pasos
1. Iniciar una nueva partida
2. Chocar intencionalmente con aviones 3 veces
3. Observar el comportamiento tras cada colisión
4. Observar la pantalla de Game Over

### Resultado esperado
- ✅ Primera colisión: vidas = 2, juego continúa
- ✅ Segunda colisión: vidas = 1, juego continúa
- ✅ Tercera colisión: vidas = 0, aparece pantalla "GAME OVER"
- ✅ Se muestra la puntuación final
- ✅ Se puede reiniciar con R o volver al menú con ESC

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 4: Pausa y reanudación

### Objetivo
Verificar que la función de pausa funciona correctamente.

### Pasos
1. Iniciar una partida
2. Durante el juego, presionar P
3. Observar que el juego se pausa
4. Presionar P nuevamente
5. Verificar que el juego continúa

### Resultado esperado
- ✅ Al presionar P aparece overlay de "PAUSA"
- ✅ Los aviones dejan de moverse
- ✅ El pájaro no responde a controles (excepto P y ESC)
- ✅ Al presionar P de nuevo, el juego continúa normalmente
- ✅ La puntuación y vidas se mantienen

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 5: Reiniciar partida

### Objetivo
Verificar que se puede reiniciar una partida después de Game Over.

### Pasos
1. Jugar hasta perder (Game Over)
2. En la pantalla de Game Over, presionar R
3. Verificar el estado del nuevo juego

### Resultado esperado
- ✅ Se inicia una nueva partida
- ✅ Puntuación regresa a 0
- ✅ Vidas regresan a 3
- ✅ El pájaro está en la posición inicial
- ✅ Los carriles están limpios (sin aviones acumulados)

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 6: Persistencia del Highscore

### Objetivo
Verificar que el récord se guarda y persiste entre sesiones.

### Pasos
1. Jugar y obtener una puntuación (ej: 500)
2. Cerrar el juego completamente
3. Abrir el archivo `highscore.json` y verificar el valor
4. Volver a ejecutar el juego
5. Verificar que el highscore se muestra correctamente
6. Jugar y superar el récord anterior
7. Verificar el mensaje "¡NUEVO RÉCORD!"
8. Cerrar y volver a abrir el juego

### Resultado esperado
- ✅ El archivo `highscore.json` contiene `{"highscore": <puntuación>}`
- ✅ Al iniciar el juego, se muestra "Récord: X" en el menú
- ✅ Al superar el récord, aparece "¡NUEVO RÉCORD!" en Game Over
- ✅ El nuevo récord persiste después de cerrar el juego

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 7: Control de sonido

### Objetivo
Verificar que se puede activar/desactivar el sonido.

### Pasos
1. Iniciar el juego
2. Comenzar partida y verificar sonido de puntos/colisión
3. Presionar M para desactivar el sonido
4. Verificar que no hay sonido
5. Presionar M para activar el sonido
6. Verificar que el sonido vuelve

### Resultado esperado
- ✅ Indicador en pantalla muestra "[M] ON" u "[M] OFF"
- ✅ El color del indicador cambia (verde = on, gris = off)
- ✅ Los sonidos se reproducen solo cuando está activado
- ✅ El cambio es instantáneo

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 8: Evitación de overlap en spawn

### Objetivo
Verificar que los aviones no aparecen superpuestos.

### Pasos
1. Modificar `config.json`: `"spawnRate": 5.0` (alto para forzar spawns)
2. Iniciar el juego
3. Observar los carriles durante 30 segundos
4. Restaurar `"spawnRate": 1.0`

### Resultado esperado
- ✅ Los aviones nunca aparecen encima de otros
- ✅ Hay un espacio mínimo entre aviones del mismo carril
- ✅ El espacio mínimo corresponde a `minSpawnDistancePx` (120 px)

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 9: Incremento de dificultad

### Objetivo
Verificar que la dificultad aumenta con el tiempo.

### Pasos
1. Iniciar una partida
2. Observar la velocidad inicial de los aviones
3. Sobrevivir al menos 30 segundos (2 incrementos de dificultad)
4. Comparar la velocidad de los nuevos aviones

### Resultado esperado
- ✅ Después de 15 segundos, los aviones son más rápidos
- ✅ Después de 30 segundos, son aún más rápidos
- ✅ El incremento es aproximadamente 8% por paso

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Prueba 10: Navegación de menús

### Objetivo
Verificar la navegación entre estados del juego.

### Pasos
1. Ejecutar el juego → Menú principal
2. Presionar ESPACIO → Juego activo
3. Presionar ESC → Menú principal
4. Presionar ESPACIO → Juego activo
5. Perder todas las vidas → Game Over
6. Presionar ESC → Menú principal
7. Presionar ESPACIO → Nuevo juego
8. En juego, presionar ESC → Salir al menú

### Resultado esperado
- ✅ ESPACIO inicia el juego desde el menú
- ✅ ESC durante el juego vuelve al menú
- ✅ R en Game Over reinicia
- ✅ ESC en Game Over vuelve al menú
- ✅ La transición es fluida sin errores

### Resultado obtenido
- [ ] PASÓ
- [ ] FALLÓ - Descripción: _______________

---

## Resumen de Pruebas

| # | Prueba | Estado |
|---|--------|--------|
| 1 | Colisión resta vida | ⬜ |
| 2 | Cruce suma puntos | ⬜ |
| 3 | Sistema de vidas y Game Over | ⬜ |
| 4 | Pausa y reanudación | ⬜ |
| 5 | Reiniciar partida | ⬜ |
| 6 | Persistencia del Highscore | ⬜ |
| 7 | Control de sonido | ⬜ |
| 8 | Evitación de overlap | ⬜ |
| 9 | Incremento de dificultad | ⬜ |
| 10 | Navegación de menús | ⬜ |

**Leyenda:** ⬜ Pendiente | ✅ Pasó | ❌ Falló

---

## Notas adicionales

### Información del entorno de prueba
- Sistema operativo: _______________
- Versión de Python: _______________
- Versión de Pygame: _______________
- Fecha de prueba: _______________
- Probador: _______________

### Bugs encontrados
1. _______________
2. _______________
3. _______________

### Sugerencias de mejora
1. _______________
2. _______________
3. _______________

