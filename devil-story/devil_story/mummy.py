
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame

## Game modules
import enemy




class Mummy(enemy.Enemy):
    def __init__(self, mummy_assets: dict, screen: pygame.Surface, playable_area_grid: list[list], grid_size) -> None:
        """Horse enemy object

        Parameters
        ----------
        mummy_assets : dict
            Mummy image and sound assets
        screen : pygame.display
            Pygame screen
        playable_area_grid : list[list]
            Matrix of bools for playable area
        """
        
        ## Assets
        self.alive_image = mummy_assets['images']['mummy_alive']
        self.dead_image = mummy_assets['images']['mummy_dead']
        self.image = self.alive_image
        self.base_image = self.image.copy()  # Store the original rotated image

        ## Stats
        self.living = True
        self.speed = 2
        self.death_time = 0.0
        self.death_cooldown = random.randint(15, 25)
        self.path = []  # Store the path calculated by A*
        self.path_update_timer = 0  # Timer to control path updates
        self.spawned = False  # Flag to check if the enemy has been spawned
        self.rotation_angle = 0  # Initial rotation angle
        self.health = 100
        self.max_health = 100

        ## Display
        self.screen = screen
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.base_image.get_rect(center=self.rect.center)
        self.hitbox_rect.height = 10
        self.hitbox_rect.width = 10
        self.playable_area_grid = playable_area_grid
        grid_size = grid_size

        super().__init__(screen, playable_area_grid, grid_size)





    def heuristic(self, a, b):
        # heuristic using Euclidean distance
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)











    def update(self, group_dict, world, current_time) -> None:
        """Update Mummy object each frame

        Parameters
        ----------
        group_dict : dict
            Dictionary of all sprite groups
        current_time : float
            Time of frame
        """
        player = group_dict['player_group'].sprites()[0]
        if not self.spawned:
            self.spawn_randomly(player.pos, 150)
        else:
            if self.path_update_timer <= 0:
                self.update_path_to_target(player.pos)
                self.path_update_timer = 100
            else:
                self.path_update_timer -= 1

            ## Move and update health if alive
            self.move_towards_target_astar(player.pos, world)
            self.draw_health_bar(self.health, self.max_health)

            # Check if the enemy has reached the player's hitbox
            if self.rect.colliderect(player.rect):
                player.health -= 100
            else:
                # Check if the enemy's health is 0 or less, and kill it

                if self.health <= 0 and self.living:
                    self.living = False
                    self.death_time = time.time()
                    self.death_cooldown = random.randint(7, 15)
                    self.image = self.dead_image
                    self.base_image = self.image.copy()
                    
                elif not self.living and current_time >= self.death_time + self.death_cooldown:
                    self.living = True
                    self.health = 100
                    self.image = self.alive_image
                    self.base_image = self.image.copy()






