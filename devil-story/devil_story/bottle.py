
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame

## Game modules
import oldman
import tools






class Bottle(pygame.sprite.Sprite):
    def __init__(self, bottle_assets: dict, screen: pygame.display, playable_area_grid: list[list]) -> None:
        """Bottle object

        Parameters
        ----------
        bottle_assets : dict
            Bottle image and sound assets
        screen : pygame.display
            Pygame screen
        playable_area_grid : list[list]
            Matrix of bools for playable area
        """        
        super().__init__()
        ## Assets
        self.image = bottle_assets['images']['bottle']
        self.base_image = self.image.copy()  # Store the original rotated image
        self.rect = self.image.get_rect()

        ## Stats
        self.spawn_timer = 0

        ## Display
        self.screen = screen
        self.hitbox_rect = self.base_image.get_rect(center=self.rect.center)
        self.playable_area_grid = playable_area_grid

        ## Spawn bottle
        self.spawn_time = time.time()
        self.lifetime = random.randint(10, 20)
        self.x, self.y = (random.randint(100, 600), random.randint(100, 600))
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def update(self, group_dict: dict, world, current_time: float) -> None:
        """Update bottle object each frame

        Parameters
        ----------
        group_dict : dict
            Dictionary of all sprite groups
        current_time : float
            Time of frame
        """
        # Check if the enemy has reached the player's hitbox
        player = group_dict['player_group'].sprites()[0]
        if self.rect.colliderect(player.rect):
            player.bottles += 1
            self.kill()
        elif pygame.sprite.spritecollideany(self, group_dict['enemy_group']) or \
             current_time >= self.spawn_time + self.lifetime:
            self.kill()


