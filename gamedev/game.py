import pygame
import sys
import random
import math
import io
import wave
import struct

pygame.init()
pygame.mixer.init(22050, -16, 1, 512)

# --- ГЕНЕРАТОР БАЗОВЫХ ЗВУКОВ ---
def make_sfx(sfx_type):
    sr = 22050
    buf = io.BytesIO()
    with wave.open(buf, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        
        if sfx_type == "step":
            samples = int(sr * 0.05)
            for i in range(samples):
                val = int(random.uniform(-5000, 5000) * (1 - i/samples))
                w.writeframesraw(struct.pack('<h', val))
                
        elif sfx_type == "dash":
            samples = int(sr * 0.2)
            for i in range(samples):
                freq = 900 - (700 * (i/samples))
                val = int(math.sin(2 * math.pi * freq * (i/sr)) * 12000 * (1 - i/samples))
                w.writeframesraw(struct.pack('<h', val))
                
    buf.seek(0)
    return pygame.mixer.Sound(buf)

# --- ГЕНЕРАТОР УНИКАЛЬНЫХ СТОНОВ (Процедурная генерация голоса) ---
def make_groan_sfx():
    sr = 22050
    buf = io.BytesIO()
    with wave.open(buf, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        
        # Случайные параметры для каждого стона
        duration = random.uniform(0.4, 0.7) # Длина от 0.4 до 0.7 секунд
        start_freq = random.uniform(130, 220) # Низкий бас (базовый тон голоса)
        end_freq = start_freq * random.uniform(0.5, 0.7) # К концу стона голос падает
        vibrato_speed = random.uniform(15, 30) # Дрожание голоса
        grit = random.uniform(0.1, 0.3) # Уровень хрипоты/искажения
        
        samples = int(sr * duration)
        
        for i in range(samples):
            t = i / sr
            progress = i / samples
            
            # 1. Плавное падение частоты
            current_freq = start_freq - (start_freq - end_freq) * progress
            
            # 2. Добавляем вибрато (легкое изменение частоты туда-сюда)
            current_freq += math.sin(2 * math.pi * vibrato_speed * t) * 10
            
            # 3. Синтезируем волну (смесь синусоиды и шума для хрипоты)
            osc = math.sin(2 * math.pi * current_freq * t)
            noise = random.uniform(-grit, grit)
            
            # Огибающая: звук плавно затухает к концу
            env = (1.0 - progress) ** 1.5 
            
            # Применяем жесткое ограничение (клиппинг) для создания 8-битного ретро-эффекта
            combined = osc + noise
            if combined > 0.8: combined = 0.8
            elif combined < -0.8: combined = -0.8
            
            val = int(combined * env * 15000)
            w.writeframesraw(struct.pack('<h', val))
            
    buf.seek(0)
    return pygame.mixer.Sound(buf)

# Создаем звуки
SND_STEP = make_sfx("step")
SND_DASH = make_sfx("dash")
# Генерируем 6 РАЗНЫХ стонов при запуске игры
SND_GROANS = [make_groan_sfx() for _ in range(6)]

# Настройки окна
WIN_W, WIN_H = 1000, 600
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("ASCII RPG - Dynamic Groans")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Consolas", 24, bold=True)
CHAR_W, CHAR_H = font.size("#")

# Палитра
C_BG = (12, 12, 18)
C_WALL = (60, 110, 200)
C_PLAYER = (80, 255, 120)
C_ENEMY = (255, 60, 80)
C_TRAP = (255, 180, 40)
C_EXIT = (200, 80, 255)
C_DASH = (220, 255, 255)
C_UI = (200, 200, 220)

level_map = [
    "########################################################################################################################",
    "#                                                                                                                      #",
    "# @                                          E                                                                         #",
    "#                                                                                                                      #",
    "#                                                                                                                      #",
    "##########     ###################################################     #######################################     #####",
    "##########     ###################################################     #######################################     #####",
    "#                                                                #     #                                     #     #",
    "#                                                                #     #                                     #     #",
    "#                E                                               #     #                 E                   #     #",
    "#                                                                #     #                                     #     #",
    "#                                                                #     #                                     #     #",
    "#####################################     ########################     ###################     ###############     #",
    "#####################################     ########################     ###################     ###############     #",
    "#                                   #     #                            #                 #     #                   #",
    "#           x                       #     #                            #        x        #     #                   #",
    "#                                   #     #       E                    #                 #     #         E         #",
    "#                                   #     #                            #                 #     #                   #",
    "#                                   #     #                            #                 #     #                   #",
    "##########     ######################     ##############################                 #     #####################",
    "##########     ######################     ##############################                 #     #####################",
    "#                                                                                        #                         #",
    "#                                                                                        #                         #",
    "#                   E                                                                    #                         #",
    "#                                                                                        #                         #",
    "#                                                                                        #                         #",
    "###############################################     ######################################                         #",
    "###############################################     ######################################                         #",
    "#                                             #     #                                                              #",
    "#                                             #     #                                                              #",
    "#                       x                     #     #                     E                                        #",
    "#                                             #     #                                                              #",
    "#                                             #     #                                                              #",
    "#########################     #################     ######################################                         #",
    "#########################     #################     ######################################                         #",
    "#                                                                                        #                         #",
    "#                                                                                        #                       > #",
    "#          E                                                  E                          #                         #",
    "#                                                                                        #                         #",
    "########################################################################################################################"
]

MAP_PIXEL_W = len(level_map[0]) * CHAR_W
MAP_PIXEL_H = len(level_map) * CHAR_H

P_SPRITES = {
    'idle': [" o ", "/|\\", "/ \\"],
    'run_r1': [" o ", " /|", " / "], 'run_r2': [" o ", " |\\", " \\ "],
    'run_l1': [" o ", "|\\ ", " \\ "], 'run_l2': [" o ", "/| ", " / "],
    'slide_r': ["   ", " _o", "/\\-"], 'slide_l': ["   ", "o_ ", "-\\/-"]
}
E_SPRITES = {
    'idle': [" v ", "/|\\", "/ \\"],
    'run_r1': [" v ", " /|", " / "], 'run_r2': [" v ", " |\\", " \\ "],
    'run_l1': [" v ", "|\\ ", " \\ "], 'run_l2': [" v ", "/| ", " / "]
}

background = pygame.Surface((MAP_PIXEL_W, MAP_PIXEL_H))
background.fill(C_BG)

walls, traps, enemies = [], [], []
exit_rect = None
start_x, start_y = 0, 0

for y, row in enumerate(level_map):
    for x, char in enumerate(row):
        rect = pygame.Rect(x * CHAR_W, y * CHAR_H, CHAR_W, CHAR_H)
        if char == '#':
            walls.append(rect)
            background.blit(font.render("#", True, C_WALL), (rect.x, rect.y))
        elif char == '@': start_x, start_y = rect.x, rect.y
        elif char == '>': exit_rect = rect
        elif char == 'x': traps.append(rect)
        elif char == 'E': enemies.append({'pos': pygame.math.Vector2(rect.x, rect.y), 'dir': random.choice([-1, 1])})

class Entity:
    def __init__(self, x, y, width, height):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, width, height)
        self.look_dir = pygame.math.Vector2(1, 0)
        self.anim_timer = 0

    def move_and_collide(self, dt):
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        hit_wall_x = False
        for w in walls:
            if self.rect.colliderect(w):
                if self.vel.x > 0: self.rect.right = w.left
                if self.vel.x < 0: self.rect.left = w.right
                self.pos.x = self.rect.x; self.vel.x = 0; hit_wall_x = True

        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)
        for w in walls:
            if self.rect.colliderect(w):
                if self.vel.y > 0: self.rect.bottom = w.top
                if self.vel.y < 0: self.rect.top = w.bottom
                self.pos.y = self.rect.y; self.vel.y = 0
        return hit_wall_x

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, CHAR_W * 2.2, CHAR_H * 2.5)
        self.accel = 3500.0
        self.friction = 0.82
        self.dash_speed = 900.0
        
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.hp = 100
        self.gold = 0
        self.step_timer = 0

    def update(self, dt, keys):
        acc = pygame.math.Vector2(0, 0)
        move_u, move_d = keys[pygame.K_w] or keys[pygame.K_UP], keys[pygame.K_s] or keys[pygame.K_DOWN]
        move_l, move_r = keys[pygame.K_a] or keys[pygame.K_LEFT], keys[pygame.K_d] or keys[pygame.K_RIGHT]

        if not self.is_dashing:
            if move_u: acc.y = -self.accel
            if move_d: acc.y = self.accel
            if move_l: acc.x = -self.accel; self.look_dir.x = -1
            if move_r: acc.x = self.accel; self.look_dir.x = 1

            if keys[pygame.K_SPACE] and self.dash_cooldown <= 0:
                self.is_dashing = True
                self.dash_timer = 0.2
                self.dash_cooldown = 0.5
                self.vel = pygame.math.Vector2(self.look_dir.x * self.dash_speed, 0)
                SND_DASH.play() 

            if self.vel.length() > 30:
                self.step_timer += dt
                if self.step_timer > 0.15:
                    SND_STEP.play()
                    self.step_timer = 0
            else:
                self.step_timer = 0

        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0: self.is_dashing = False
        else:
            if self.dash_cooldown > 0: self.dash_cooldown -= dt
            self.vel += acc * dt
            self.vel *= (self.friction ** (dt * 60))
            if self.vel.length() < 0.1: self.vel = pygame.math.Vector2(0, 0)

        self.move_and_collide(dt)
        self.anim_timer += dt

    def draw(self, surface, cam_x, cam_y):
        breath_y = math.sin(pygame.time.get_ticks() * 0.005) * 3 if self.vel.length() < 10 else 0
        if self.is_dashing:
            lines, color = (P_SPRITES['slide_r'] if self.look_dir.x >= 0 else P_SPRITES['slide_l']), C_DASH
        elif self.vel.length() > 30:
            frame = int(self.anim_timer * 10) % 2
            if self.look_dir.x > 0: lines = P_SPRITES['run_r1'] if frame == 0 else P_SPRITES['run_r2']
            else: lines = P_SPRITES['run_l1'] if frame == 0 else P_SPRITES['run_l2']
            color = C_PLAYER
        else:
            lines, color = P_SPRITES['idle'], C_PLAYER

        for i, line in enumerate(lines):
            surface.blit(font.render(line, True, color), (self.rect.x - cam_x, self.rect.y - cam_y + i * (CHAR_H * 0.75) + breath_y))

class Enemy(Entity):
    def __init__(self, x, y, direction):
        super().__init__(x, y, CHAR_W * 2.2, CHAR_H * 2.5)
        self.speed = 120
        self.look_dir.x = direction

    def update(self, dt):
        self.vel.x = self.speed * self.look_dir.x
        if self.move_and_collide(dt): self.look_dir.x *= -1
        self.anim_timer += dt

    def draw(self, surface, cam_x, cam_y):
        frame = int(self.anim_timer * 8) % 2
        lines = (E_SPRITES['run_r1'] if frame == 0 else E_SPRITES['run_r2']) if self.look_dir.x > 0 else (E_SPRITES['run_l1'] if frame == 0 else E_SPRITES['run_l2'])
        for i, line in enumerate(lines):
            surface.blit(font.render(line, True, C_ENEMY), (self.rect.x - cam_x, self.rect.y - cam_y + i * (CHAR_H * 0.75)))

player = Player(start_x, start_y)
enemy_objects = [Enemy(e['pos'].x, e['pos'].y, e['dir']) for e in enemies]

cam_x, cam_y = 0, 0
running = True

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    player.update(dt, pygame.key.get_pressed())

    cam_x += (player.rect.centerx - WIN_W // 2 - cam_x) * 5 * dt
    cam_y += (player.rect.centery - WIN_H // 2 - cam_y) * 5 * dt
    cam_x, cam_y = max(0, min(cam_x, MAP_PIXEL_W - WIN_W)), max(0, min(cam_y, MAP_PIXEL_H - WIN_H))

    for t in traps[:]:
        if player.rect.colliderect(t):
            player.hp -= 5; player.gold += 50; traps.remove(t)

    for e in enemy_objects[:]:
        e.update(dt)
        if player.rect.colliderect(e.rect):
            if player.is_dashing:
                enemy_objects.remove(e)
                player.gold += 40
                
                # ВОСПРОИЗВЕДЕНИЕ СЛУЧАЙНОГО СТОНА ПРИ УБИЙСТВЕ
                random.choice(SND_GROANS).play()
                
            else:
                player.hp -= 15
                enemy_objects.remove(e)

    screen.blit(background, (-cam_x, -cam_y))
    for t in traps: screen.blit(font.render("x", True, C_TRAP), (t.x - cam_x, t.y - cam_y))
    if exit_rect: screen.blit(font.render(">", True, C_EXIT), (exit_rect.x - cam_x, exit_rect.y - cam_y))
    
    for e in enemy_objects: e.draw(screen, cam_x, cam_y)
    player.draw(screen, cam_x, cam_y)

    pygame.draw.rect(screen, (20, 20, 30), (0, WIN_H - 40, WIN_W, 40))
    screen.blit(font.render(f"HP: {player.hp} | GOLD: {player.gold} | ENEMIES: {len(enemy_objects)} | [WASD] Бег  [SPACE] Рывок", True, C_UI), (20, WIN_H - 35))

    pygame.display.flip()
    if player.hp <= 0 or (exit_rect and player.rect.colliderect(exit_rect)): running = False

pygame.quit()