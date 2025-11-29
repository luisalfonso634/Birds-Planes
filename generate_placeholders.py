#!/usr/bin/env python3
"""
generate_placeholders.py
========================
Script para generar sprites placeholder en formato PNG para Birds & Planes.
Ejecutar este script antes de correr el juego si no tienes los assets.

Uso:
    python generate_placeholders.py

Genera:
    - assets/bird_1.png, bird_2.png, bird_3.png (animación del pájaro)
    - assets/plane_small.png, plane_med.png, plane_large.png (aviones)
    - assets/background.png (fondo con montañas y ciudad)
"""

import os
import struct
import zlib

def create_png(width, height, pixels):
    """
    Crea un archivo PNG desde una lista de píxeles RGBA.
    pixels: lista de tuplas (r, g, b, a) de tamaño width * height
    """
    def make_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        chunk_crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
        return chunk_len + chunk_type + data + chunk_crc

    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk (imagen comprimida)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # Filter byte
        for x in range(width):
            idx = y * width + x
            r, g, b, a = pixels[idx]
            raw_data += bytes([r, g, b, a])
    
    compressed = zlib.compress(raw_data, 9)
    idat = make_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = make_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend


def create_bird_frame(frame_num):
    """Crea un frame del pájaro (32x32 píxeles)."""
    width, height = 32, 32
    pixels = [(0, 0, 0, 0)] * (width * height)  # Transparente
    
    # Colores del pájaro
    body_color = (255, 200, 50, 255)      # Amarillo
    wing_color = (255, 150, 0, 255)       # Naranja
    eye_color = (0, 0, 0, 255)            # Negro
    beak_color = (255, 100, 0, 255)       # Naranja oscuro
    
    # Cuerpo (círculo central)
    for y in range(10, 24):
        for x in range(8, 24):
            dx = x - 16
            dy = y - 17
            if dx*dx + dy*dy <= 49:  # Radio ~7
                pixels[y * width + x] = body_color
    
    # Ala (posición varía según frame para animación)
    wing_offset = [0, -2, 0][frame_num]
    for y in range(12 + wing_offset, 18 + wing_offset):
        for x in range(4, 12):
            if y >= 0 and y < height:
                pixels[y * width + x] = wing_color
    
    # Ojo
    pixels[14 * width + 20] = eye_color
    pixels[14 * width + 21] = eye_color
    pixels[15 * width + 20] = eye_color
    pixels[15 * width + 21] = eye_color
    
    # Pico
    for y in range(16, 19):
        for x in range(24, 28):
            pixels[y * width + x] = beak_color
    
    return width, height, pixels


def create_plane(size_type):
    """Crea un avión según tamaño: 'small', 'med', 'large'."""
    sizes = {
        'small': (48, 24),
        'med': (64, 32),
        'large': (80, 40)
    }
    width, height = sizes[size_type]
    pixels = [(0, 0, 0, 0)] * (width * height)
    
    # Colores del avión
    body_colors = {
        'small': (100, 150, 255, 255),   # Azul claro
        'med': (200, 200, 200, 255),     # Gris
        'large': (255, 100, 100, 255)    # Rojo
    }
    body_color = body_colors[size_type]
    window_color = (50, 50, 80, 255)
    wing_color = (80, 80, 80, 255)
    
    # Fuselaje (cuerpo principal)
    body_y_start = height // 3
    body_y_end = height * 2 // 3
    for y in range(body_y_start, body_y_end):
        for x in range(width // 6, width - width // 8):
            pixels[y * width + x] = body_color
    
    # Cabina (punta)
    for y in range(body_y_start, body_y_end):
        for x in range(width - width // 8, width - 2):
            pixels[y * width + x] = window_color
    
    # Alas
    wing_y = height // 2
    for y in range(wing_y - height // 4, wing_y + height // 4):
        for x in range(width // 3, width // 2):
            if y >= 0 and y < height:
                pixels[y * width + x] = wing_color
    
    # Cola
    for y in range(height // 6, body_y_start + 2):
        for x in range(0, width // 5):
            if y >= 0 and y < height:
                pixels[y * width + x] = wing_color
    
    return width, height, pixels


def create_background():
    """Crea el fondo con cielo, montañas y ciudad (800x600)."""
    width, height = 800, 600
    pixels = []
    
    # Colores
    sky_top = (135, 206, 250)       # Azul cielo claro
    sky_bottom = (200, 230, 255)    # Azul más claro
    mountain_color = (100, 120, 140) # Gris azulado
    mountain_snow = (230, 240, 250)  # Blanco nieve
    city_color = (60, 60, 80)        # Gris oscuro ciudad
    window_color = (255, 255, 150)   # Amarillo ventanas
    
    for y in range(height):
        for x in range(width):
            # Gradiente de cielo
            t = y / height
            r = int(sky_top[0] * (1-t) + sky_bottom[0] * t)
            g = int(sky_top[1] * (1-t) + sky_bottom[1] * t)
            b = int(sky_top[2] * (1-t) + sky_bottom[2] * t)
            
            # Montañas (en la parte inferior)
            mountain_height = 150
            mountain_base = height - 100
            if y > mountain_base - mountain_height:
                # Simular montañas con triángulos
                peak1 = abs((x % 200) - 100) * 1.5
                peak2 = abs(((x + 80) % 150) - 75) * 1.8
                mountain_line = mountain_base - max(peak1, peak2)
                
                if y > mountain_line:
                    if y < mountain_line + 20:
                        r, g, b = mountain_snow
                    else:
                        r, g, b = mountain_color
            
            # Ciudad (edificios en primer plano)
            city_base = height - 80
            if y > city_base:
                # Edificios con alturas variables
                building_width = 40 + (x // 50) % 30
                building_height = 50 + (hash(x // 40) % 60)
                building_top = height - building_height
                
                if y > building_top:
                    # Es parte de un edificio
                    r, g, b = city_color
                    
                    # Ventanas
                    local_x = x % 40
                    local_y = (y - building_top) % 20
                    if 5 < local_x < 15 and 5 < local_y < 12:
                        if hash((x // 40, y // 20)) % 3 != 0:  # Algunas apagadas
                            r, g, b = window_color
                    elif 25 < local_x < 35 and 5 < local_y < 12:
                        if hash((x // 40 + 1, y // 20)) % 3 != 0:
                            r, g, b = window_color
            
            pixels.append((r, g, b, 255))
    
    return width, height, pixels


def main():
    """Genera todos los assets placeholder."""
    # Crear directorio assets si no existe
    os.makedirs('assets', exist_ok=True)
    
    print("Generando assets placeholder para Birds & Planes...")
    print("-" * 50)
    
    # Generar frames del pájaro
    for i in range(3):
        w, h, px = create_bird_frame(i)
        png_data = create_png(w, h, px)
        filename = f'assets/bird_{i+1}.png'
        with open(filename, 'wb') as f:
            f.write(png_data)
        print(f"✓ Creado: {filename} ({w}x{h} píxeles)")
    
    # Generar aviones
    for size in ['small', 'med', 'large']:
        w, h, px = create_plane(size)
        png_data = create_png(w, h, px)
        filename = f'assets/plane_{size}.png'
        with open(filename, 'wb') as f:
            f.write(png_data)
        print(f"✓ Creado: {filename} ({w}x{h} píxeles)")
    
    # Generar fondo
    print("Generando fondo (puede tomar unos segundos)...")
    w, h, px = create_background()
    png_data = create_png(w, h, px)
    filename = 'assets/background.png'
    with open(filename, 'wb') as f:
        f.write(png_data)
    print(f"✓ Creado: {filename} ({w}x{h} píxeles)")
    
    print("-" * 50)
    print("¡Todos los assets generados exitosamente!")
    print("\nAhora puedes ejecutar el juego con: python main.py")


if __name__ == '__main__':
    main()

