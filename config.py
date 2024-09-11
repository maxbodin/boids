from pygame import Vector3

screen_width = 2000
screen_height = 1500

fps = 60
poids_cohesion = 0.1
poids_alignement = 0.1
poids_separation = 0.3
poids_circling = 0

boid_size: float = 10
boid_min_size: float = 2
boid_max_size: float = 20

blue_boid_color: Vector3 = (0, 0, 255)
red_boid_color: Vector3 = (255, 0, 0)

boid_n_neighbours = 20

boid_sep_distance = 30
boid_kill_distance = 10

boid_speed = 100
boid_max_speed = 150

nombre_boids = 800
taille_cellule = 50

all_boids = []