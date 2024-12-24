
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame

## Game modules
from level import Level




class newEnemy(pygame.sprite.Sprite):
    def __init__(self, assets: dict, screen: pygame.Surface, world: Level) -> None:
        """_summary_

        Parameters
        ----------
        assets : dict
            _description_
        health : int
            _description_
        max_health : int
            _description_
        screen : pygame.Surface
            _description_
        world : Level
            _description_
        """
        super().__init__()

        self.assets = assets
        self.screen = screen
        self.world = world




    def draw_health_bar(self, enemy_pos: tuple, health: int, max_health: int) -> None:
        """Draw mummy health bar on game screen
        """
        ## Scale health and draw healthbar background
        health_ratio = health / max_health
        bar_width, bar_height = 40, 5
        health_bar_width = int(bar_width * health_ratio)
        health_bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(health_bar_surface, (255, 255, 255), (0, 0, bar_width, bar_height))

        ## Set color for current health percentage
        if health_ratio > 0.6:
            color = (0, 255, 0)  # Green
        elif health_ratio > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        ## Draw bar on enemy
        pygame.draw.rect(health_bar_surface, color, (0, 0, health_bar_width, bar_height))
        health_bar_pos = (enemy_pos[0] - bar_width // 2, enemy_pos[1] - 10)
        self.screen.blit(health_bar_surface, health_bar_pos)









