import pygame
import config
from pygame import Vector2, Vector3
from drawable import Drawable
from math import cos, sin, atan2, pi
import time
import random

class Boid(Drawable):

    # DO NOT TOUCH

    #config vars
    _size: float = config.boid_size
    _color: Vector3 = config.good_boid_color
    _n_neighbours = config.boid_n_neighbours
    _sep_distance = config.boid_sep_distance
    _speed = config.boid_speed

    def __init__(self, x:float, y:float) -> None:
        super().__init__()
        self._pos: Vector2 = Vector2(x, y)
        self._vel: Vector2 = Vector2(1,0)
        self._color = config.good_boid_color if random.random() < 0.5 else config.bad_boid_color
        self._speed += random.randint(40, 100)

    def getPos(self) -> Vector2:
        return self._pos

    def setPos(self, x: float, y: float):
        self._pos = Vector2(x, y)

    def getVelocity(self):
        return self._vel
    
    def setVelocity(self, vel: Vector2):
        self._vel = vel.normalize()
        
    def get_cell(self, pos: Vector2) -> tuple:
        # Utiliser le modulo pour que les cellules "s'enroulent" autour des bords
        cell_x = int((pos.x // config.taille_cellule) % (config.screen_width // config.taille_cellule))
        cell_y = int((pos.y // config.taille_cellule) % (config.screen_height // config.taille_cellule))
        return cell_x, cell_y
    
    def organize_in_grid(self, boids: list['Boid']):
        grid = {}
        for boid in boids:
            cell = self.get_cell(boid.getPos())
            if cell not in grid:
                grid[cell] = []
            grid[cell].append(boid)
        return grid
    
    def get_neighbours_in_grid(self, grid) -> list['Boid']:
        neighbours = []
        current_cell = self.get_cell(self.getPos())

        # Chercher dans la cellule courante et les 8 cellules adjacentes
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Utiliser le modulo pour les cellules adjacentes en tenant compte des bords
                neighbour_cell_x = (current_cell[0] + dx) % (config.screen_width // config.taille_cellule)
                neighbour_cell_y = (current_cell[1] + dy) % (config.screen_height // config.taille_cellule)
                neighbour_cell = (neighbour_cell_x, neighbour_cell_y)
                

                if neighbour_cell in grid:
                    neighbours.extend(grid[neighbour_cell])

        # Retirer le boid lui-même de la liste des voisins
        return [b for b in neighbours if b != self]
    
    def toroidal_distance(self, boid: 'Boid') -> float:
        delta_x = min(abs(self._pos.x - boid._pos.x), config.screen_width - abs(self._pos.x - boid._pos.x))
        delta_y = min(abs(self._pos.y - boid._pos.y), config.screen_height - abs(self._pos.y - boid._pos.y))
        
        return (delta_x ** 2 + delta_y ** 2) ** 0.5
    
    def closest_neighbours(self, grid) -> list['Boid']:
        # Récupérer tous les voisins à partir de la grille
        neighbours = self.get_neighbours_in_grid(grid)
        
        # Trier les voisins par distance torique
        sorted_neighbours = sorted(neighbours, key=lambda boid: self.toroidal_distance(boid))
        
        # Limiter à config.nombre_voisins voisins les plus proches
        return sorted_neighbours[:config.boid_n_neighbours]

    def move(self, delta: float):
        self._pos = self._pos + self._vel * delta * self._speed
        self.wrap_around()
    
    def draw(self, screen):
        _dir = atan2(self._vel.y, self._vel.x)
        triangle = [
            Vector2(cos(_dir) * self._size, sin(_dir) * self._size),
            Vector2(cos(_dir + pi * (3/4)) * self._size, sin(_dir + pi * (3/4)) * self._size),
            Vector2(cos(_dir + pi * (5/4)) * self._size, sin(_dir + pi * (5/4)) * self._size)
        ]
        points = [(p.x + self._pos.x, p.y + self._pos.y) for p in triangle]
        pygame.draw.polygon(screen, self._color, points)

    # ----------------------------------------------------
    
    """
    La séparation permet d'éviter aux boids une collision avec un voisin. Pour celà on veut récupérer tous les voisins et en retirer un vecteur non normalisé pour chaque voisin en dessous de la distance minimale. La somme de ces vecteurs nous donne une force de séparation qui n'est donc pas normalisée, ce qui lui donne un poids variable."""
    def separation(self, boids: list['Boid']) -> Vector2:
        steer = Vector2(0, 0)
        count = 0
        kill_steer = Vector2(0, 0)
        kill_count = 0

        for boid in boids:
            distance = self.toroidal_distance(boid)

            # Check if the boid has a different color
            if self._color != boid._color and distance < config.boid_kill_distance:
                # Steer towards this boid (war behavior)
                direction_to_boid = (boid.getPos() - self._pos).normalize()
                kill_steer += direction_to_boid
                kill_count += 1
                self._size += 2 if self._size < config.boid_max_size else 0
                boid._size -= 5 if boid._size < config.boid_min_size else 0

                if boid in config.all_boids and boid._size <= config.boid_min_size: 
                    config.all_boids.remove(boid)
                    
            elif 0 < distance < self._sep_distance:
                # Normal separation behavior
                diff = self._pos - boid.getPos()
                diff = diff.normalize() / distance  # Weight by distance
                steer += diff
                count += 1

        # Average the steering forces
        if count > 0:
            steer /= count

        if kill_count > 0:
            kill_steer /= kill_count

        # Normalize the final steering vectors
        if steer.length() > 0:
            steer = steer.normalize()

        if kill_steer.length() > 0:
            kill_steer = kill_steer.normalize()

        # If there are boids to kill (with different colors), prioritize killing steer over avoiding others
        return kill_steer if kill_count > 0 else steer


    """
    Le premier comportement que nous allons ajouter à nos boids est l'alignement. Le nom de ce comportement est assez descriptif, le but est bien d'aligner nos boids. Pour obtenir un vecteur relativement aligné, il suffit de faire la moyenne des vélocités des autres boids (et possiblement normaliser ce vecteur).
    """
    def alignement(self, boids: list['Boid']) -> Vector2:
        avg_velocity = Vector2(0, 0)
        count = 0

        for boid in boids:
            avg_velocity += boid.getVelocity()
            count += 1

        if count > 0:
            avg_velocity /= count  # Compute the average velocity
            avg_velocity = avg_velocity.normalize()  # Normalize it to get the direction to align

        return avg_velocity
    
    """
    La cohésion consiste à diriger un boid vers le centre de la nuée, c'est-à-dire la moyenne des positions de chaque boids de la nuée. Ce comportement peut aussi potentiellement bénéficier d'une normalisation.
    """
    def cohesion(self, boids: list['Boid']) -> Vector2:
        center_of_mass = Vector2(0, 0)
        count = 0

        for boid in boids:
            center_of_mass += boid.getPos()
            count += 1

        if count > 0:
            center_of_mass /= count  # Compute the average position
            direction_to_com = (center_of_mass - self._pos).normalize()  # Normalize to get direction
            return direction_to_com
        else:
            return Vector2(0, 0)  # Return zero vector if there are no neighbors
    
    # Bordures toriques
    def wrap_around(self):
        # Si le boid dépasse la bordure droite, il réapparaît à la bordure gauche
        if self._pos.x > config.screen_width:
            self._pos.x = 0
        # Si le boid dépasse la bordure gauche, il réapparaît à la bordure droite
        elif self._pos.x < 0:
            self._pos.x = config.screen_width
        
        # Si le boid dépasse la bordure basse, il réapparaît en haut
        if self._pos.y > config.screen_height:
            self._pos.y = 0
        # Si le boid dépasse la bordure haute, il réapparaît en bas
        elif self._pos.y < 0:
            self._pos.y = config.screen_height

    def circling(self, w, h):
        return ( (Vector2(w/2, h/2) + Vector2(cos(time.time()), sin(time.time()))) - self._pos).normalize()