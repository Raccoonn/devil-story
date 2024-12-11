
## Standard Library
import sys
import math
import heapq
import random

## Third Party
import pygame

## Game modules
import tools




class Level:
    def __init__(self, world_assets: dict) -> None:
        """Define level objects within class

        Parameters
        ----------
        world_assets : dict
            All world assets
                - walls
                - fences
        """

        self.wall_image = pygame.transform.scale(world_assets['images']['church'], (200, 200))

        

        self.walls = [self.wall_image.get_rect(center=(400, 300))]
        self.wall_color = (255, 0, 0)


        self.fence_image = world_assets['images']['fence']

        self.fences = [self.fence_image.get_rect(center=(200, 600)), self.fence_image.get_rect(center=(600, 600)) ]
        self.fence_color = (0, 0, 255)



