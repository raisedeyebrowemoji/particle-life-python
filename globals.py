import pygame
import config

def clamp(value, minv, maxv):
    return min(max(value, minv), maxv)

def hsv_to_color(h, s, v):
    color = pygame.Color(0,0,0)
    color.hsva = (h, s, v)
    return color


grid = {}

def add_to_grid(particle):
    cell_x = int(particle.position.x // config.GRID_SIZE)
    cell_y = int(particle.position.y // config.GRID_SIZE)
    grid.setdefault((cell_x, cell_y), []).append(particle)

def reset_grid():
    global grid
    grid = {}

def get_neighbor_particles(particle):
    cell_x = int(particle.position.x // config.GRID_SIZE)
    cell_y = int(particle.position.y // config.GRID_SIZE)
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            neighbors.extend(grid.get((cell_x + dx, cell_y + dy), []))
    return neighbors
    
def draw_debug_grid(screen):
    for x in range(0, config.SCREEN_WIDTH, config.GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, config.SCREEN_HEIGHT))
    for y in range(0, config.SCREEN_HEIGHT, config.GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (config.SCREEN_WIDTH, y))
