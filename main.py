import pygame
import random
import particle
from particle import Particle
import config
import importlib
import globals

pygame.init()

# Setup
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

particles = []

current_type = 0

# Function to create a single particle
def create_particle(spawn_point, type):
    spawn_point = pygame.Vector2(spawn_point)
    particle = Particle(spawn_point, config.particle_size, type)
    particles.append(particle)
    globals.add_to_grid(particle)
    return particle

# Function to create multiple particles
def create_particles(amount):
    global current_type
    for _ in range(amount):
        while True:  # Keep trying until a valid spawn position is found
            new_position = pygame.Vector2(
                random.randint(0, config.SCREEN_WIDTH),
                random.randint(0, config.SCREEN_HEIGHT)
            )
            if all((new_position - p.position).magnitude() > 5 for p in particles):
                break  # Found a valid position

        create_particle(new_position, current_type % config.types)
        current_type += 1
    current_type = 0


create_particles(config.particles)

grid = {}

debug = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                
                past_types = config.types

                importlib.reload(config)
                if config.particles > len(particles):
                    create_particles(config.particles-len(particles))
                elif config.particles < len(particles):
                    particles = particles[:config.particles]
                


            if event.key == pygame.K_1:
                current_type = 1
            elif event.key == pygame.K_2:
                current_type = 2
            elif event.key == pygame.K_3:
                current_type = 3
            elif event.key == pygame.K_4:
                current_type = 4
            elif event.key == pygame.K_5:
                current_type = 5
            elif event.key == pygame.K_6:
                current_type = 6
            elif event.key == pygame.K_7:
                current_type = 7
            elif event.key == pygame.K_8:
                current_type = 8
            elif event.key == pygame.K_9:
                current_type = 9
            elif event.key == pygame.K_0:
                current_type = 0
            
            if event.key == pygame.K_d:
                debug = not debug

    # Spawn particles if mouse button is pressed
    if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is held
        create_particle(pygame.mouse.get_pos(), current_type)

    globals.reset_grid()
    for particle in particles:
        globals.add_to_grid(particle)

    # Update particles
    for particle in particles:
        particle.process(globals.grid)

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen with black
    for particle in particles:
        particle.draw(screen)
    if debug:
        globals.draw_debug_grid(screen)
        for particle in particles:
            if particle.type == current_type:
                particle.draw_connections(screen)

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
