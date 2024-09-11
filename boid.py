import pygame
import config
from pygame import Vector2, Vector3
from drawable import Drawable
from math import cos, sin, atan2, pi
import time

class Boid(Drawable):

    # DO NOT TOUCH

    #config vars
    _size: float = config.boid_size
    _color: Vector3 = config.boid_color
    _n_neighbours = config.boid_n_neighbours
    _sep_distance = config.boid_sep_distance
    _speed = config.boid_speed

    def __init__(self, x:float, y:float) -> None:
        super().__init__()
        self._pos: Vector2 = Vector2(x, y)
        self._vel: Vector2 = Vector2(1,0)

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
    
    def separation(self, boids: list['Boid']) -> Vector2:
        # TODO
        return Vector2(1,0)

    def alignement(self, boids: list['Boid']) -> Vector2:
        # TODO
        return Vector2(1,0)
    
    def cohesion(self, boids: list['Boid']) -> Vector2:
        # TODO
        return Vector2(1,0)
    
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