
## Standard Library
import sys
import math
import heapq
import random

## Third Party
import pygame
import networkx as nx

## Game modules
import tools




class Level:
    def __init__(self, width: int, height: int, grid_size: int, world_assets: dict) -> None:
        """Define level objects within class

        Parameters
        ----------
        world_assets : dict
            All world assets
                - walls
                - fences
        """
        ## Basic dimensions of game world
        self.width, self.height = width, height
        self.grid_size = grid_size

        ## World assets
        self.wall_image = pygame.transform.scale(world_assets['images']['church'], (200, 200))
        self.walls = [self.wall_image.get_rect(topleft=(200, 200))]
        self.wall_color = (255, 0, 0)

        self.fence_image = pygame.transform.scale(world_assets['images']['fence'], (50, 50))
        self.fences = [self.fence_image.get_rect(topleft=(200, 600)), self.fence_image.get_rect(topleft=(600, 600))]
        self.fence_color = (0, 0, 255)

        ## Store all world objects
        self.objects = [*self.walls, *self.fences]

        ## Make world graph
        self.make_playable_area()



    def make_playable_area(self) -> None:
        """_summary_
        """
        ## Setup base 2d grid graph and update node data with coordinates
        self.G = nx.grid_2d_graph(self.width // self.grid_size, self.height // self.grid_size)
        node_attr = {}
        for row, y in enumerate(range(0, self.width, self.grid_size)):
            for col, x in enumerate(range(0, self.height, self.grid_size)):
                node_attr[(col, row)] = {'coords': (x + self.grid_size // 2, y + self.grid_size // 2)}
        nx.set_node_attributes(self.G, node_attr)

        ## Remove any nodes that collide with world objects
        for node in list(self.G.nodes()):
            for obj in self.objects:
                if obj.collidepoint(self.G.nodes[node]['coords']):
                    self.G.remove_node(node)
                    break
        
        ## Define playable area by setting all to False - Then update based on valid nodes in world graph
        self.playable_area = [[False] * (self.width // self.grid_size) for _ in  range(self.height // self.grid_size)]
        for node in self.G.nodes():
            self.playable_area[node[0]][node[1]] = True
        


    def check_los(self, pos: tuple, target_pos: tuple) -> bool:
        """_summary_

        Parameters
        ----------
        pos : tuple
            _description_
        target_pos : tuple
            _description_

        Returns
        -------
        bool
            _description_
        """
        for wall in self.walls:
            if wall.clipline(*pos, *target_pos):
                return False
            
        for fence in self.fences:
            if fence.clipline(*pos, *target_pos):
                return False
            
        return True



