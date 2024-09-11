import pygame
from pygame import Vector2
import config
from boid import Boid
import random

pygame.init()

fps = config.fps
screen = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("py-boid")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial" , 12 , bold = False)

# fps display util function
def fps_counter():
    fps= f"{int(clock.get_fps())} FPS"
    fps_t = font.render(fps, 1, pygame.Color("GREEN"))
    screen.blit(fps_t,(15,15))

config.all_boids = [Boid(random.randint(0, config.screen_width), random.randint(0,config.screen_height)) for i in range(config.nombre_boids)]
for boid in config.all_boids :
    _pos = boid.getPos()
    boid.setPos(_pos.x + random.randint(0, 150), _pos.y + random.randint(-15, 15))

## Main render loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta = clock.tick(fps)/1000

    # Fill the screen with a background color
    screen.fill((255, 255, 255))
    
    grid = boid.organize_in_grid(config.all_boids )

    blue_boid: int = 0
    red_boid: int = 0
    # Draw all boids
    for boid in config.all_boids:
        velocity = boid.getVelocity()
        closests = boid.closest_neighbours(grid)
        # TODO: call your boid logic here
        alignement = boid.alignement(closests)
        cohesion = boid.cohesion(closests)
        separation = boid.separation(closests)
        circling = boid.circling(config.screen_width, config.screen_height)
        velocity += cohesion * config.poids_cohesion + alignement * config.poids_alignement + separation * config.poids_separation + circling * config.poids_circling
        # -------------------------------
        boid.setVelocity(velocity)
        boid.move(delta)
        boid.draw(screen)

        if boid._color == config.red_boid_color:
            red_boid += 1
        elif  boid._color == config.blue_boid_color:
            blue_boid += 1


    red_boid_counter= f"{int(red_boid)} RED BOID"
    red_boid_r = font.render(red_boid_counter, 1, pygame.Color("RED"))
    screen.blit(red_boid_r,(15,40))

    blue_boid_counter= f"{int(blue_boid)} BLUE BOID"
    blue_boid_r = font.render(blue_boid_counter, 1, pygame.Color("BLUE"))
    screen.blit(blue_boid_r,(15,80))

    # Draw the fps counter
    fps_counter()

    # Update the display
    pygame.display.update()