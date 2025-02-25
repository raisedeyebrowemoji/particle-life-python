import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
CENTER = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

FPS = 60

particles = 1000
particle_size = 3

types = 6

force_scale = 0.0005
friction = 0.8

forces = [[random.uniform(-25, 25) for _ in range(types)] for _ in range(types)]

mindistances = [[random.uniform(15, 30) for _ in range(types)] for _ in range(types)]

radii = [[random.uniform(50, 200) for _ in range(types)] for _ in range(types)]

max_radius = max([max(row) for row in radii])


GRID_SIZE = round(max_radius*2/3)

print(GRID_SIZE)

EDGE_MODE = 'WRAP_FULL'