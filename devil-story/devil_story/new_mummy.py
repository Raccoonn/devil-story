
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame
import networkx as nx

## Game modules
import new_enemy
from level import Level






class Mummy(new_enemy.newEnemy):
    def __init__(self, assets: dict, screen: pygame.Surface, world: Level) -> None:
        """_summary_

        Parameters
        ----------
        assets : dict
            _description_
        screen : pygame.Surface
            _description_
        world : Level
            _description_
        """
        super().__init__(assets, screen, world)

        ## Stats
        self.speed = 2
        self.living = False
        self.death_time = 0.0
        self.death_cooldown = random.randint(15, 25)
        self.health = 100
        self.max_health = 100

        self.last_update = 0

        self.alive_image = assets['images']['mummy_alive']
        self.dead_image = assets['images']['mummy_dead']  
        self.base_image = self.alive_image.copy()


    def random_position(self, player_pos: tuple, min_distance: int) -> None:
        """_summary_

        Parameters
        ----------
        player_pos : pygame.math.Vector2
            _description_
        min_distance : int
            _description_
        """
        while True:
            pos = pygame.math.Vector2(random.choice(list(self.world.G.nodes)))
            pos = pygame.math.Vector2(pos.x * self.world.grid_size + self.world.grid_size // 2, pos.y * self.world.grid_size + self.world.grid_size // 2)
            if pygame.math.Vector2(player_pos).distance_to(pos) >= min_distance:
                break

        self.living = True
        self.image = self.assets['images']['mummy_alive']

        hitbox_size = 20
        self.hitbox = pygame.Rect(pos.x, pos.y, hitbox_size, hitbox_size)
        self.rect = self.image.get_rect(center=self.hitbox.center)

        return


    
    def get_path(self, player_pos: tuple) -> None:
        """_summary_

        Parameters
        ----------
        player_pos : tuple
            _description_
        """
        pos_1 = (self.hitbox.centerx // self.world.grid_size, self.hitbox.centery // self.world.grid_size)
        pos_2 = (player_pos[0] // self.world.grid_size, player_pos[1] // self.world.grid_size)
        self.path = [self.world.G.nodes[node]['coords'] for node in nx.shortest_path(self.world.G, pos_1, pos_2)]




    def random_path(self):
        raise NotImplemented



    def move(self):
        for next_point in reversed(self.path):

            target_x = next_point[0]
            target_y = next_point[1]

            try:
                direction = pygame.math.Vector2(target_x - self.hitbox.centerx, target_y - self.hitbox.centery).normalize()
            except:
                direction = pygame.math.Vector2(self.hitbox.x, self.hitbox.y).normalize()
            
            new_rect = self.hitbox.move(direction.x * self.speed, direction.y * self.speed)

            grid_x = int(new_rect.centerx / self.world.grid_size)
            grid_y = int(new_rect.centery / self.world.grid_size)
            

            if (0 <= grid_x < len(self.world.playable_area[0]) and
                0 <= grid_y < len(self.world.playable_area) and
                self.world.playable_area[grid_x][grid_y] and
                self.world.check_los(new_rect.center, (target_x, target_y))
                ):
                self.hitbox = new_rect
                break

        angle = math.degrees(math.atan2(target_y - self.hitbox.centery, target_x - self.hitbox.centerx))
        self.image = pygame.transform.rotate(self.base_image, -angle - 90)
        self.rect = self.image.get_rect(center=self.hitbox.center)






    def update(self, group_dict, world, current_time):

        player = group_dict['player_group'].sprites()[0]

        if self.living:

            if current_time > self.last_update + 1:
                self.last_update = current_time
                self.get_path(group_dict['player_group'].sprites()[0].hitbox_rect.center)

            self.move()
            self.draw_health_bar(self.hitbox.midtop, self.health, self.max_health)

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


        





