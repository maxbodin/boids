from pygame import Vector3

screen_width = 1500
screen_height = 1000
fps = 60
poids_cohesion = 0.1
poids_alignement = 0.1
poids_separation = 0.3
poids_circling = 0.1

boid_size: float = 7
boid_color: Vector3 = (0, 0, 0)
boid_n_neighbours = 10
boid_sep_distance = 35
boid_speed = 100

nombre_boids = 100
taille_cellule = 50