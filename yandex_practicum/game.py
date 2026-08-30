import math
import pygame
import sys

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Самонаводящаяся ракета (sin/cos в динамике)")
clock = pygame.time.Clock()

# Начальные координаты ракеты (в центре экрана)
rocket_x, rocket_y = 400.0, 300.0
rocket_angle = 0.0          # Текущий угол, куда смотрит ракета
SPEED = 8.0                 # Постоянная скорость полета ракеты
ROTATION_SPEED = 0.05    # Скорость поворота ракеты (затухание маневра)

# Рисуем ракету (острый треугольник)
rocket_surface = pygame.Surface((80, 40), pygame.SRCALPHA)
pygame.draw.polygon(rocket_surface, (255, 69, 0), [(0, 0), (80, 20), (0, 40)])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. Получаем координаты цели (мыши)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 2. Вычисляем угол ИДЕАЛЬНОГО направления на цель
    dx = mouse_x - rocket_x
    dy = mouse_y - rocket_y
    target_angle = math.atan2(dy, dx)

    # 3. Плавный разворот ракеты к цели
    # Находим кратчайшую разницу между текущим углом и нужным
    angle_diff = target_angle - rocket_angle
    angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))
    
    # Ракета поворачивается не мгновенно, а с затуханием (на 5% за кадр)
    rocket_angle += angle_diff * ROTATION_SPEED

    # 4. ДВИЖЕНИЕ: Раскладываем скорость по осям X и Y с помощью sin и cos
    # Зная угол, мы проецируем скорость SPEED на координатную сетку
    rocket_x += SPEED * math.cos(rocket_angle)
    rocket_y += SPEED * math.sin(rocket_angle)

    # 5. ОТРИСОВКА
    screen.fill((20, 20, 30))

    # Поворачиваем картинку ракеты (переводим радианы в градусы)
    # Минус нужен из-за перевернутой оси Y в графических движках
    rotated_rocket = pygame.transform.rotate(rocket_surface, -math.degrees(rocket_angle))
    new_rect = rotated_rocket.get_rect(center=(int(rocket_x), int(rocket_y)))

    screen.blit(rotated_rocket, new_rect.topleft)
    pygame.display.flip()
    clock.tick(60)
