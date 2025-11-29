#!/usr/bin/env python3
"""
Birds & Planes
==============
Un juego tipo Frogger donde controlas un pájaro que debe cruzar carriles
evitando aviones. Desarrollado con Python y Pygame.

Compatible con Pygbag para versión web y dispositivos móviles.

Controles:
- Flechas direccionales / Touch: Mover el pájaro
- P: Pausar/Reanudar
- M: Activar/Desactivar sonido
- R: Reiniciar (en Game Over)
- ESC: Salir al menú / Cerrar juego

Autor: Birds & Planes Team
Licencia: MIT
"""

import pygame
import json
import os
import random
import sys
import asyncio
from typing import List, Dict, Tuple, Optional

# ============================================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================================

# Ruta del directorio del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 50)
ORANGE = (255, 150, 50)
LIGHT_BLUE = (100, 150, 255)


def load_config() -> Dict:
    """
    Carga la configuración desde config.json.
    Si no existe, usa valores por defecto.
    """
    config_path = os.path.join(BASE_DIR, 'config.json')
    default_config = {
        "numLanes": 5,
        "lives": 3,
        "pointsPerCross": 100,
        "spawnRate": 1.0,
        "planeSpeedRange": [150, 320],
        "difficultyStepEveryXSeconds": 15,
        "difficultySpeedMultiplier": 1.08,
        "minSpawnDistancePx": 120,
        "screenWidth": 800,
        "screenHeight": 600,
        "birdSpeed": 200,
        "laneHeight": 80,
        "soundEnabled": True
    }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            for key, value in default_config.items():
                if key not in loaded:
                    loaded[key] = value
            return loaded
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Advertencia: No se pudo cargar config.json ({e}). Usando valores por defecto.")
        return default_config


def load_highscore() -> int:
    """Carga el highscore desde highscore.json."""
    highscore_path = os.path.join(BASE_DIR, 'highscore.json')
    try:
        with open(highscore_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('highscore', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def save_highscore(score: int) -> bool:
    """Guarda el highscore en highscore.json."""
    highscore_path = os.path.join(BASE_DIR, 'highscore.json')
    try:
        with open(highscore_path, 'w', encoding='utf-8') as f:
            json.dump({'highscore': score}, f, indent=2)
        return True
    except IOError as e:
        print(f"Error al guardar highscore: {e}")
        return False


# ============================================================================
# CONTROLES TÁCTILES PARA MÓVILES
# ============================================================================

class TouchControls:
    """Controles táctiles virtuales para dispositivos móviles."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Tamaño de botones
        self.btn_size = 60
        self.btn_margin = 10
        
        # Posición del D-pad (esquina inferior izquierda)
        self.dpad_x = self.btn_margin + self.btn_size
        self.dpad_y = screen_height - self.btn_margin - self.btn_size * 2
        
        # Rectángulos de los botones
        self.btn_up = pygame.Rect(
            self.dpad_x, 
            self.dpad_y - self.btn_size, 
            self.btn_size, self.btn_size
        )
        self.btn_down = pygame.Rect(
            self.dpad_x, 
            self.dpad_y + self.btn_size, 
            self.btn_size, self.btn_size
        )
        self.btn_left = pygame.Rect(
            self.dpad_x - self.btn_size, 
            self.dpad_y, 
            self.btn_size, self.btn_size
        )
        self.btn_right = pygame.Rect(
            self.dpad_x + self.btn_size, 
            self.dpad_y, 
            self.btn_size, self.btn_size
        )
        
        # Botón de acción (esquina inferior derecha)
        self.btn_action = pygame.Rect(
            screen_width - self.btn_margin - self.btn_size * 2,
            screen_height - self.btn_margin - self.btn_size * 2,
            self.btn_size * 2,
            self.btn_size * 2
        )
        
        # Estado de los botones
        self.pressing = {
            'up': False, 'down': False, 'left': False, 'right': False, 'action': False
        }
        
        # Touch activos
        self.active_touches = {}
    
    def handle_touch_down(self, pos: Tuple[int, int], touch_id: int = 0):
        """Maneja el inicio de un toque."""
        self.active_touches[touch_id] = pos
        self._update_button_states(pos, True)
    
    def handle_touch_up(self, touch_id: int = 0):
        """Maneja el fin de un toque."""
        if touch_id in self.active_touches:
            del self.active_touches[touch_id]
        
        # Resetear estados si no hay más toques
        if not self.active_touches:
            for key in self.pressing:
                self.pressing[key] = False
    
    def handle_touch_move(self, pos: Tuple[int, int], touch_id: int = 0):
        """Maneja el movimiento de un toque."""
        self.active_touches[touch_id] = pos
        # Resetear y recalcular
        for key in self.pressing:
            self.pressing[key] = False
        for t_pos in self.active_touches.values():
            self._update_button_states(t_pos, True)
    
    def _update_button_states(self, pos: Tuple[int, int], pressed: bool):
        """Actualiza el estado de los botones basado en la posición del toque."""
        if self.btn_up.collidepoint(pos):
            self.pressing['up'] = pressed
        elif self.btn_down.collidepoint(pos):
            self.pressing['down'] = pressed
        elif self.btn_left.collidepoint(pos):
            self.pressing['left'] = pressed
        elif self.btn_right.collidepoint(pos):
            self.pressing['right'] = pressed
        elif self.btn_action.collidepoint(pos):
            self.pressing['action'] = pressed
    
    def get_keys_pressed(self) -> Dict[int, bool]:
        """Retorna un diccionario compatible con el sistema de teclas."""
        return {
            pygame.K_UP: self.pressing['up'],
            pygame.K_DOWN: self.pressing['down'],
            pygame.K_LEFT: self.pressing['left'],
            pygame.K_RIGHT: self.pressing['right'],
            pygame.K_SPACE: self.pressing['action'],
        }
    
    def is_action_pressed(self) -> bool:
        """Retorna True si el botón de acción fue presionado."""
        return self.pressing['action']
    
    def draw(self, screen: pygame.Surface, alpha: int = 100):
        """Dibuja los controles táctiles en pantalla."""
        # Superficie semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        btn_color = (*LIGHT_BLUE, alpha)
        btn_pressed_color = (*GREEN, alpha + 50)
        text_color = (*WHITE, 200)
        
        # Dibujar D-pad
        buttons = [
            (self.btn_up, 'up', '▲'),
            (self.btn_down, 'down', '▼'),
            (self.btn_left, 'left', '◄'),
            (self.btn_right, 'right', '►'),
        ]
        
        for rect, key, symbol in buttons:
            color = btn_pressed_color if self.pressing[key] else btn_color
            pygame.draw.rect(overlay, color, rect, border_radius=10)
            pygame.draw.rect(overlay, (*WHITE, 150), rect, 2, border_radius=10)
            
            # Símbolo
            font = pygame.font.Font(None, 36)
            text = font.render(symbol, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            overlay.blit(text, text_rect)
        
        # Dibujar botón de acción
        action_color = btn_pressed_color if self.pressing['action'] else btn_color
        pygame.draw.circle(overlay, action_color, self.btn_action.center, self.btn_size)
        pygame.draw.circle(overlay, (*WHITE, 150), self.btn_action.center, self.btn_size, 3)
        
        font = pygame.font.Font(None, 24)
        text = font.render("TAP", True, text_color)
        text_rect = text.get_rect(center=self.btn_action.center)
        overlay.blit(text, text_rect)
        
        screen.blit(overlay, (0, 0))


# ============================================================================
# CLASES DEL JUEGO
# ============================================================================

class Bird(pygame.sprite.Sprite):
    """Clase que representa al pájaro (jugador)."""
    
    def __init__(self, x: int, y: int, config: Dict):
        super().__init__()
        self.config = config
        self.speed = config['birdSpeed']
        
        self.frames = self._load_frames()
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.last_lane = -1
        self.crossed_lanes = set()
    
    def _load_frames(self) -> List[pygame.Surface]:
        """Carga los frames de animación del pájaro."""
        frames = []
        assets_dir = os.path.join(BASE_DIR, 'assets')
        
        for i in range(1, 4):
            path = os.path.join(assets_dir, f'bird_{i}.png')
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (40, 40))
                frames.append(img)
            except pygame.error:
                surf = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(surf, YELLOW, (20, 20), 15)
                pygame.draw.circle(surf, ORANGE, (20, 15 + i*2), 8)
                pygame.draw.circle(surf, BLACK, (28, 15), 3)
                pygame.draw.polygon(surf, ORANGE, [(32, 20), (40, 18), (40, 22)])
                frames.append(surf)
        
        return frames
    
    def update(self, dt: float, keys_pressed: Dict[int, bool], 
               screen_width: int, screen_height: int, safe_zone_height: int):
        """Actualiza la posición y animación del pájaro."""
        dx, dy = 0, 0
        if keys_pressed.get(pygame.K_LEFT, False):
            dx = -self.speed * dt
        if keys_pressed.get(pygame.K_RIGHT, False):
            dx = self.speed * dt
        if keys_pressed.get(pygame.K_UP, False):
            dy = -self.speed * dt
        if keys_pressed.get(pygame.K_DOWN, False):
            dy = self.speed * dt
        
        self.rect.x += dx
        self.rect.y += dy
        
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
        
        if self.rect.bottom > screen_height - safe_zone_height + self.rect.height:
            self.rect.bottom = screen_height - safe_zone_height + self.rect.height
        
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    def reset_position(self, x: int, y: int):
        """Resetea la posición del pájaro."""
        self.rect.center = (x, y)
        self.crossed_lanes.clear()
        self.last_lane = -1
    
    def get_current_lane(self, lane_rects: List[pygame.Rect]) -> int:
        """Retorna el índice del carril actual."""
        for i, lane_rect in enumerate(lane_rects):
            if lane_rect.colliderect(self.rect):
                return i
        return -1


class Plane(pygame.sprite.Sprite):
    """Clase que representa un avión enemigo."""
    
    _image_cache: Dict[str, pygame.Surface] = {}
    
    def __init__(self, lane_index: int, lane_y: int, direction: int, 
                 speed: float, plane_type: str, screen_width: int):
        super().__init__()
        
        self.lane_index = lane_index
        self.direction = direction
        self.speed = speed
        self.plane_type = plane_type
        self.screen_width = screen_width
        
        self.image = self._load_image(plane_type, direction)
        self.rect = self.image.get_rect()
        
        if direction > 0:
            self.rect.right = 0
        else:
            self.rect.left = screen_width
        
        self.rect.centery = lane_y
        self.x = float(self.rect.x)
    
    @classmethod
    def _load_image(cls, plane_type: str, direction: int) -> pygame.Surface:
        """Carga y cachea la imagen del avión."""
        cache_key = f"{plane_type}_{direction}"
        
        if cache_key in cls._image_cache:
            return cls._image_cache[cache_key]
        
        assets_dir = os.path.join(BASE_DIR, 'assets')
        path = os.path.join(assets_dir, f'plane_{plane_type}.png')
        
        sizes = {'small': (50, 25), 'med': (70, 35), 'large': (90, 45)}
        size = sizes.get(plane_type, (70, 35))
        
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
        except pygame.error:
            img = pygame.Surface(size, pygame.SRCALPHA)
            colors = {'small': BLUE, 'med': GRAY, 'large': RED}
            color = colors.get(plane_type, GRAY)
            
            pygame.draw.ellipse(img, color, (0, size[1]//4, size[0], size[1]//2))
            pygame.draw.polygon(img, DARK_GRAY, [
                (size[0]//3, size[1]//2),
                (size[0]//2, 0),
                (size[0]//2, size[1])
            ])
            pygame.draw.ellipse(img, (50, 50, 80), 
                              (size[0]-size[0]//4, size[1]//3, size[0]//5, size[1]//3))
        
        if direction < 0:
            img = pygame.transform.flip(img, True, False)
        
        cls._image_cache[cache_key] = img
        return img
    
    def update(self, dt: float):
        """Actualiza la posición del avión."""
        self.x += self.speed * self.direction * dt
        self.rect.x = int(self.x)
    
    def is_off_screen(self) -> bool:
        """Retorna True si el avión salió de la pantalla."""
        if self.direction > 0:
            return self.rect.left > self.screen_width
        else:
            return self.rect.right < 0


class Lane:
    """Representa un carril donde aparecen aviones."""
    
    def __init__(self, index: int, y: int, height: int, direction: int,
                 config: Dict, screen_width: int):
        self.index = index
        self.y = y
        self.height = height
        self.direction = direction
        self.config = config
        self.screen_width = screen_width
        
        self.planes: List[Plane] = []
        self.spawn_timer = random.uniform(0, 1.0 / config['spawnRate'])
        
        self.plane_types = ['small', 'med', 'large']
        self.type_weights = [0.5, 0.35, 0.15]
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(0, self.y - self.height // 2, 
                          self.screen_width, self.height)
    
    def _get_spawn_rate(self, difficulty_multiplier: float) -> float:
        return self.config['spawnRate'] * difficulty_multiplier
    
    def _get_speed_range(self, difficulty_multiplier: float) -> Tuple[float, float]:
        base_min, base_max = self.config['planeSpeedRange']
        return (base_min * difficulty_multiplier, base_max * difficulty_multiplier)
    
    def _can_spawn(self) -> bool:
        min_distance = self.config['minSpawnDistancePx']
        
        for plane in self.planes:
            if self.direction > 0:
                if plane.rect.left < min_distance:
                    return False
            else:
                if plane.rect.right > self.screen_width - min_distance:
                    return False
        
        return True
    
    def _choose_plane_type(self) -> str:
        return random.choices(self.plane_types, weights=self.type_weights)[0]
    
    def update(self, dt: float, difficulty_multiplier: float) -> List[Plane]:
        new_planes = []
        
        for plane in self.planes[:]:
            plane.update(dt)
            if plane.is_off_screen():
                self.planes.remove(plane)
        
        spawn_rate = self._get_spawn_rate(difficulty_multiplier)
        self.spawn_timer -= dt
        
        if self.spawn_timer <= 0:
            self.spawn_timer = 1.0 / spawn_rate + random.uniform(-0.3, 0.3)
            
            if self._can_spawn():
                speed_min, speed_max = self._get_speed_range(difficulty_multiplier)
                speed = random.uniform(speed_min, speed_max)
                plane_type = self._choose_plane_type()
                
                plane = Plane(
                    lane_index=self.index,
                    lane_y=self.y,
                    direction=self.direction,
                    speed=speed,
                    plane_type=plane_type,
                    screen_width=self.screen_width
                )
                
                self.planes.append(plane)
                new_planes.append(plane)
        
        return new_planes
    
    def clear(self):
        self.planes.clear()


class GameUI:
    """Maneja la interfaz de usuario."""
    
    def __init__(self, screen: pygame.Surface, config: Dict):
        self.screen = screen
        self.config = config
        self.width = config['screenWidth']
        self.height = config['screenHeight']
        
        pygame.font.init()
        try:
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 32)
        except:
            self.font_large = pygame.font.SysFont('arial', 72)
            self.font_medium = pygame.font.SysFont('arial', 48)
            self.font_small = pygame.font.SysFont('arial', 32)
    
    def draw_menu(self, highscore: int):
        """Dibuja el menú principal."""
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(DARK_GRAY)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("BIRDS & PLANES", True, YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 4))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_small.render("Esquiva los aviones!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 4 + 50))
        self.screen.blit(subtitle, subtitle_rect)
        
        hs_text = self.font_medium.render(f"Record: {highscore}", True, ORANGE)
        hs_rect = hs_text.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.screen.blit(hs_text, hs_rect)
        
        # Instrucciones adaptadas para móvil y PC
        instructions = [
            "PC: Flechas para mover",
            "Movil: Usa los controles tactiles",
            "",
            "TOCA o presiona ESPACIO"
        ]
        
        y_offset = self.height // 2 + 40
        for line in instructions:
            text = self.font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 35
    
    def draw_hud(self, score: int, lives: int, highscore: int, 
                 sound_on: bool, paused: bool):
        """Dibuja el HUD durante el juego."""
        pygame.draw.rect(self.screen, (0, 0, 0, 150), (0, 0, self.width, 45))
        
        score_text = self.font_small.render(f"Puntos: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.font_small.render("Vidas: ", True, WHITE)
        self.screen.blit(lives_text, (self.width // 2 - 80, 10))
        
        for i in range(lives):
            pygame.draw.circle(self.screen, RED, 
                             (self.width // 2 + i * 25, 22), 8)
        
        hs_text = self.font_small.render(f"Record: {highscore}", True, ORANGE)
        hs_rect = hs_text.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(hs_text, hs_rect)
        
        if paused:
            pause_overlay = pygame.Surface((self.width, self.height))
            pause_overlay.fill(BLACK)
            pause_overlay.set_alpha(150)
            self.screen.blit(pause_overlay, (0, 0))
            
            pause_text = self.font_large.render("PAUSA", True, WHITE)
            pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(pause_text, pause_rect)
            
            resume_text = self.font_small.render("Toca para continuar", True, GRAY)
            resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(resume_text, resume_rect)
    
    def draw_game_over(self, score: int, highscore: int, is_new_record: bool):
        """Dibuja la pantalla de Game Over."""
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(DARK_GRAY)
        overlay.set_alpha(220)
        self.screen.blit(overlay, (0, 0))
        
        go_text = self.font_large.render("GAME OVER", True, RED)
        go_rect = go_text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(go_text, go_rect)
        
        score_text = self.font_medium.render(f"Puntuacion: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        if is_new_record:
            record_text = self.font_medium.render("NUEVO RECORD!", True, YELLOW)
            record_rect = record_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
            self.screen.blit(record_text, record_rect)
        else:
            hs_text = self.font_small.render(f"Record: {highscore}", True, ORANGE)
            hs_rect = hs_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
            self.screen.blit(hs_text, hs_rect)
        
        restart_text = self.font_small.render("TOCA para reiniciar", True, GRAY)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height * 2 // 3 + 30))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_safe_zone(self, y: int, height: int):
        """Dibuja la zona segura."""
        zone_rect = pygame.Rect(0, y, self.width, height)
        pygame.draw.rect(self.screen, (50, 150, 50, 100), zone_rect)
        pygame.draw.line(self.screen, GREEN, (0, y), (self.width, y), 2)
    
    def draw_finish_zone(self, y: int, height: int):
        """Dibuja la zona de llegada."""
        zone_rect = pygame.Rect(0, y, self.width, height)
        pygame.draw.rect(self.screen, (50, 50, 150, 100), zone_rect)
        pygame.draw.line(self.screen, BLUE, (0, y + height), (self.width, y + height), 2)
        
        flag_text = self.font_small.render("META!", True, WHITE)
        flag_rect = flag_text.get_rect(center=(self.width // 2, y + height // 2))
        self.screen.blit(flag_text, flag_rect)


class GameScene:
    """Escena principal del juego."""
    
    STATE_MENU = 'menu'
    STATE_PLAYING = 'playing'
    STATE_PAUSED = 'paused'
    STATE_GAME_OVER = 'game_over'
    
    def __init__(self, screen: pygame.Surface, config: Dict):
        self.screen = screen
        self.config = config
        self.width = config['screenWidth']
        self.height = config['screenHeight']
        
        self.background = self._load_background()
        self.ui = GameUI(screen, config)
        self.touch_controls = TouchControls(self.width, self.height)
        
        self.highscore = load_highscore()
        
        self.state = self.STATE_MENU
        self.score = 0
        self.lives = config['lives']
        self.sound_enabled = config.get('soundEnabled', True)
        self.is_new_record = False
        
        self.game_time = 0
        self.difficulty_multiplier = 1.0
        
        self.safe_zone_height = 60
        self.finish_zone_y = 50
        self.finish_zone_height = 50
        
        self._create_lanes()
        
        start_x = self.width // 2
        start_y = self.height - self.safe_zone_height // 2
        self.bird = Bird(start_x, start_y, config)
        
        self.all_sprites = pygame.sprite.Group()
        self.plane_sprites = pygame.sprite.Group()
        
        self._load_sounds()
    
    def _load_background(self) -> pygame.Surface:
        """Carga la imagen de fondo."""
        path = os.path.join(BASE_DIR, 'assets', 'background.png')
        try:
            bg = pygame.image.load(path).convert()
            return pygame.transform.scale(bg, (self.width, self.height))
        except pygame.error:
            bg = pygame.Surface((self.width, self.height))
            for y in range(self.height):
                t = y / self.height
                r = int(135 * (1-t) + 200 * t)
                g = int(206 * (1-t) + 230 * t)
                b = int(250 * (1-t) + 255 * t)
                pygame.draw.line(bg, (r, g, b), (0, y), (self.width, y))
            return bg
    
    def _load_sounds(self):
        """Carga los efectos de sonido."""
        self.sounds = {}
        try:
            pygame.mixer.init()
            collision_sound = pygame.mixer.Sound(buffer=bytes([
                int(128 + 100 * (i % 20 < 10 and 1 or -1) * max(0, 1 - i/1000))
                for i in range(2000)
            ]))
            collision_sound.set_volume(0.3)
            self.sounds['collision'] = collision_sound
            
            point_sound = pygame.mixer.Sound(buffer=bytes([
                int(128 + 80 * (i % 8 < 4 and 1 or -1) * max(0, 1 - i/800))
                for i in range(1500)
            ]))
            point_sound.set_volume(0.2)
            self.sounds['point'] = point_sound
        except pygame.error:
            print("Advertencia: No se pudo inicializar el sistema de sonido.")
            self.sounds = {}
    
    def _play_sound(self, sound_name: str):
        """Reproduce un sonido si está habilitado."""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def _create_lanes(self):
        """Crea los carriles del juego."""
        self.lanes: List[Lane] = []
        num_lanes = self.config['numLanes']
        
        play_area_top = self.finish_zone_y + self.finish_zone_height
        play_area_bottom = self.height - self.safe_zone_height
        play_area_height = play_area_bottom - play_area_top
        
        lane_spacing = play_area_height / num_lanes
        
        for i in range(num_lanes):
            lane_y = int(play_area_top + lane_spacing * (i + 0.5))
            direction = 1 if i % 2 == 0 else -1
            
            lane = Lane(
                index=i,
                y=lane_y,
                height=int(lane_spacing),
                direction=direction,
                config=self.config,
                screen_width=self.width
            )
            self.lanes.append(lane)
    
    def _reset_game(self):
        """Reinicia el juego."""
        self.score = 0
        self.lives = self.config['lives']
        self.game_time = 0
        self.difficulty_multiplier = 1.0
        self.is_new_record = False
        
        for lane in self.lanes:
            lane.clear()
        
        self.plane_sprites.empty()
        
        start_x = self.width // 2
        start_y = self.height - self.safe_zone_height // 2
        self.bird.reset_position(start_x, start_y)
    
    def _check_collisions(self) -> bool:
        """Verifica colisiones AABB."""
        bird_rect = self.bird.rect.inflate(-10, -10)
        
        for lane in self.lanes:
            for plane in lane.planes:
                plane_rect = plane.rect.inflate(-5, -5)
                if bird_rect.colliderect(plane_rect):
                    return True
        
        return False
    
    def _check_lane_cross(self) -> bool:
        """Verifica si el pájaro cruzó un carril."""
        lane_rects = [lane.rect for lane in self.lanes]
        current_lane = self.bird.get_current_lane(lane_rects)
        
        if self.bird.rect.top <= self.finish_zone_y + self.finish_zone_height:
            self.score += self.config['pointsPerCross'] * 2
            self._play_sound('point')
            
            start_x = self.width // 2
            start_y = self.height - self.safe_zone_height // 2
            self.bird.reset_position(start_x, start_y)
            
            return True
        
        if current_lane >= 0 and current_lane not in self.bird.crossed_lanes:
            self.bird.crossed_lanes.add(current_lane)
            self.score += self.config['pointsPerCross']
            self._play_sound('point')
            return True
        
        return False
    
    def _update_difficulty(self, dt: float):
        """Actualiza la dificultad."""
        self.game_time += dt
        
        step_time = self.config['difficultyStepEveryXSeconds']
        multiplier = self.config['difficultySpeedMultiplier']
        
        steps = int(self.game_time / step_time)
        self.difficulty_multiplier = multiplier ** steps
    
    def _handle_collision(self):
        """Maneja una colisión."""
        self._play_sound('collision')
        self.lives -= 1
        
        if self.lives <= 0:
            if self.score > self.highscore:
                self.highscore = self.score
                save_highscore(self.highscore)
                self.is_new_record = True
            self.state = self.STATE_GAME_OVER
        else:
            start_x = self.width // 2
            start_y = self.height - self.safe_zone_height // 2
            self.bird.reset_position(start_x, start_y)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Procesa eventos de entrada."""
        # Manejar eventos táctiles
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.touch_controls.handle_touch_down(event.pos)
            
            # Acciones según estado
            if self.state == self.STATE_MENU:
                self._reset_game()
                self.state = self.STATE_PLAYING
            elif self.state == self.STATE_PAUSED:
                self.state = self.STATE_PLAYING
            elif self.state == self.STATE_GAME_OVER:
                self._reset_game()
                self.state = self.STATE_PLAYING
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.touch_controls.handle_touch_up()
        
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                self.touch_controls.handle_touch_move(event.pos)
        
        # Manejar eventos de teclado
        elif event.type == pygame.KEYDOWN:
            if self.state == self.STATE_MENU:
                if event.key == pygame.K_SPACE:
                    self._reset_game()
                    self.state = self.STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    return False
            
            elif self.state == self.STATE_PLAYING:
                if event.key == pygame.K_p:
                    self.state = self.STATE_PAUSED
                elif event.key == pygame.K_m:
                    self.sound_enabled = not self.sound_enabled
                elif event.key == pygame.K_ESCAPE:
                    self.state = self.STATE_MENU
            
            elif self.state == self.STATE_PAUSED:
                if event.key == pygame.K_p:
                    self.state = self.STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.state = self.STATE_MENU
            
            elif self.state == self.STATE_GAME_OVER:
                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                    self._reset_game()
                    self.state = self.STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.state = self.STATE_MENU
        
        return True
    
    def update(self, dt: float, keys_pressed: Dict[int, bool]):
        """Actualiza la lógica del juego."""
        if self.state != self.STATE_PLAYING:
            return
        
        # Combinar teclas físicas con controles táctiles
        touch_keys = self.touch_controls.get_keys_pressed()
        combined_keys = {**keys_pressed}
        for key, value in touch_keys.items():
            if value:
                combined_keys[key] = True
        
        self._update_difficulty(dt)
        
        self.bird.update(dt, combined_keys, self.width, self.height, 
                        self.safe_zone_height)
        
        for lane in self.lanes:
            new_planes = lane.update(dt, self.difficulty_multiplier)
            for plane in new_planes:
                self.plane_sprites.add(plane)
        
        if self._check_collisions():
            self._handle_collision()
        
        self._check_lane_cross()
    
    def draw(self):
        """Dibuja la escena del juego."""
        self.screen.blit(self.background, (0, 0))
        
        if self.state == self.STATE_MENU:
            self.ui.draw_menu(self.highscore)
        
        elif self.state in [self.STATE_PLAYING, self.STATE_PAUSED]:
            self.ui.draw_safe_zone(self.height - self.safe_zone_height, 
                                   self.safe_zone_height)
            self.ui.draw_finish_zone(self.finish_zone_y, self.finish_zone_height)
            
            for lane in self.lanes:
                y = lane.y
                pygame.draw.line(self.screen, (100, 100, 100, 100), 
                               (0, y - lane.height // 2), 
                               (self.width, y - lane.height // 2), 1)
            
            for lane in self.lanes:
                for plane in lane.planes:
                    self.screen.blit(plane.image, plane.rect)
            
            self.screen.blit(self.bird.image, self.bird.rect)
            
            # Dibujar controles táctiles
            self.touch_controls.draw(self.screen)
            
            self.ui.draw_hud(self.score, self.lives, self.highscore,
                           self.sound_enabled, self.state == self.STATE_PAUSED)
        
        elif self.state == self.STATE_GAME_OVER:
            self.ui.draw_safe_zone(self.height - self.safe_zone_height,
                                   self.safe_zone_height)
            self.ui.draw_finish_zone(self.finish_zone_y, self.finish_zone_height)
            
            for lane in self.lanes:
                for plane in lane.planes:
                    self.screen.blit(plane.image, plane.rect)
            
            self.screen.blit(self.bird.image, self.bird.rect)
            
            self.ui.draw_game_over(self.score, self.highscore, self.is_new_record)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

async def main():
    """Punto de entrada principal del juego."""
    pygame.init()
    
    config = load_config()
    
    screen = pygame.display.set_mode((config['screenWidth'], config['screenHeight']))
    pygame.display.set_caption("Birds & Planes")
    
    try:
        icon_path = os.path.join(BASE_DIR, 'assets', 'bird_1.png')
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
    except:
        pass
    
    clock = pygame.time.Clock()
    FPS = 60
    
    game = GameScene(screen, config)
    
    keys_pressed = {}
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys_pressed[event.key] = True
                if not game.handle_event(event):
                    running = False
            elif event.type == pygame.KEYUP:
                keys_pressed[event.key] = False
            else:
                game.handle_event(event)
        
        game.update(dt, keys_pressed)
        game.draw()
        
        pygame.display.flip()
        
        await asyncio.sleep(0)
    
    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
