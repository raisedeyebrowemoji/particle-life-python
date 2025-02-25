import pygame
import config
import globals
import random



class Particle:

    


    def __init__(self, spawn: pygame.Vector2, radius: float, type):
        self.position: pygame.Vector2 = spawn
        self.color: pygame.Color = globals.hsv_to_color(360/config.types*(type+1), 100, 100)
        self.radius: float = radius
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.type: int = type
        self.debug = False

    
    def get_neighbors(self, grid):
        cell_x = int(self.position.x // config.GRID_SIZE)
        cell_y = int(self.position.y // config.GRID_SIZE)
        neighbors = []
        
        # Get grid dimensions
        grid_width = config.SCREEN_WIDTH // config.GRID_SIZE
        grid_height = config.SCREEN_HEIGHT // config.GRID_SIZE
        
        # Check the current cell and all 8 neighboring cells with wrapping
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Calculate wrapped cell indices
                wrapped_x = (cell_x + dx) % grid_width
                wrapped_y = (cell_y + dy) % grid_height
                
                # Add neighbors from the wrapped cell
                neighbors.extend(grid.get((wrapped_x, wrapped_y), []))
        
        return neighbors



    def process(self, grid):
        # Update stuff
        self.radius = config.particle_size


        # Move
        direction = pygame.Vector2(0, 0)
        total_force = pygame.Vector2(0, 0)
        acceleration = pygame.Vector2(0, 0)
        distance = 0.0

        swarm = self.get_neighbors(grid)


        for particle in swarm:
            if particle != self:
                # Find raw direction
                direction = particle.position.copy()
                direction -= self.position

                # Handle wrap mode
                if config.EDGE_MODE == 'WRAP_FULL':
                    if direction.x > 0.5*config.SCREEN_WIDTH:
                        direction.x -= config.SCREEN_WIDTH
                    if direction.x < -0.5*config.SCREEN_WIDTH:
                        direction.x += config.SCREEN_WIDTH
                    if direction.y > 0.5*config.SCREEN_HEIGHT:
                        direction.y -= config.SCREEN_HEIGHT
                    if direction.y < -0.5*config.SCREEN_HEIGHT:
                        direction.y += config.SCREEN_HEIGHT
                    
                # Randomise direction if points are on one another
                if direction == pygame.Vector2(0, 0):
                    direction = pygame.Vector2(random.uniform(-1*config.radii[self.type][particle.type], config.radii[self.type][particle.type]), random.uniform(-1*config.radii[self.type][particle.type], config.radii[self.type][particle.type]))
                
                # Get distance between points
                distance = direction.magnitude()

                # Skip if it's more than sense radius
                if distance > config.radii[self.type][particle.type]:
                    continue

                # Prepare more variables
                direction = direction.normalize()

                force = direction.copy()

                base_interaction_force = config.forces[self.type][particle.type]

                # Apply repelling force
                if distance < config.mindistances[self.type][particle.type]:
                    force *= abs(base_interaction_force)*-5 # apply base repelling force
                    force *= config.mindistances[self.type][particle.type]/distance # scale based on distance

                # Apply primary force
                elif distance < config.radii[self.type][particle.type]:
                    force *= base_interaction_force
                    force *= distance/config.mindistances[self.type][particle.type]

                # Get and apply force, total force, acceleration, velocity
                force *= config.force_scale
                total_force += force
        acceleration += total_force
        self.velocity += acceleration
        self.velocity *= config.friction
        
        self.position += self.velocity

        
        # Wrap position
        if config.EDGE_MODE.__contains__('WRAP'):
            self.position.x = (self.position.x+config.SCREEN_WIDTH)%config.SCREEN_WIDTH
            self.position.y = (self.position.y+config.SCREEN_HEIGHT)%config.SCREEN_HEIGHT
        
        # Clamp position to borders
        elif config.EDGE_MODE == 'WALL':
            self.position.x = globals.clamp(self.position.x, 0+self.radius, config.SCREEN_WIDTH-self.radius)
            self.position.y = globals.clamp(self.position.y, 0+self.radius, config.SCREEN_HEIGHT-self.radius)
        
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def draw_connections(self, screen):
        for neighbor in self.get_neighbors(globals.grid):
                nx, ny = neighbor.position
                if (neighbor.position-self.position).magnitude() > config.radii[self.type][neighbor.type]:
                    continue
                pygame.draw.line(screen, self.color, (self.position.x, self.position.y), (nx, ny), 1)
