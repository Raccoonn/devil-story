
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




class Horse(new_enemy.newEnemy):
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

        ## Assets
        self.image = assets['images']['horse']
        self.base_image = self.image.copy()  # Store the original rotated image

        self.neigh_sounds = [v for k,v in assets['sounds'].items() if 'neigh' in k]

        self.neigh_time = 0
        self.neigh_cooldown = random.randint(5, 15)

        ## Stats
        self.living = True
        self.speed = 3

        self.health = 500
        self.max_health = 500
        self.rest = 0
        self.show = True

        self.random_position()


    def random_position(self) -> None:
        """Designate path by selecting two wall locations
            - Moves as set speed along straight line
        """

        sample = random.sample([1, 2, 3, 4], 2)
        high = 1000
        low = -200
        walls = {
                 1 : (random.randint(low, high), low),
                 2 : (high, random.randint(low, high)),
                 3 : (random.randint(low, high), high),
                 4 : (low, random.randint(low, high))
                 }

        self.start  = pygame.math.Vector2(walls[sample[0]])
        self.finish = pygame.math.Vector2(walls[sample[1]])
        self.speed = random.randint(3, 7)

        self.pos = self.start

        ## Update rotation
        angle = math.degrees(math.atan2(self.finish[1] - self.start[1], self.finish[0] - self.start[0]))
        self.image = pygame.transform.rotate(self.base_image, -angle - 90)

        hitbox_size = 20
        self.hitbox = pygame.Rect(self.start[0], self.start[1], hitbox_size, hitbox_size)
        self.rect = self.image.get_rect(center=self.hitbox.center)







    def get_path(self, marker_pos: tuple) -> None:
        """_summary_

        Parameters
        ----------
        player_pos : tuple
            _description_
        """
        pos_1 = (self.hitbox.centerx // self.world.grid_size, self.hitbox.centery // self.world.grid_size)
        pos_2 = (marker_pos[0] // self.world.grid_size, marker_pos[1] // self.world.grid_size)
        self.path = [self.world.G.nodes[node]['coords'] for node in nx.shortest_path(self.world.G, pos_1, pos_2)]




    def move(self):

        if (self.finish.distance_to(self.hitbox.center) < 200 or 
            not -300 < self.hitbox.centerx < 1200 or
            not -300 < self.hitbox.centery < 1200
            ):
            self.random_position()



        if 100 < self.hitbox.centerx < 700 and 100 < self.hitbox.centery < 700:

            if self.finish[0] < 1:
                tar_x = 1
            elif self.finish[0] > 700:
                tar_x = 700
            else:
                tar_x = self.finish[0]

            if self.finish[1] < 1:
                tar_y = 1
            elif self.finish[1] > 700:
                tar_y = 700
            else:
                tar_y = self.finish[1]

            marker_pos = pygame.math.Vector2((tar_x, tar_y))

            self.get_path(marker_pos)

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
                
                if (self.world.playable_area[grid_x][grid_y] and
                    self.world.check_los(new_rect.center, (target_x, target_y))
                    ):
                    self.hitbox = new_rect
                    angle = math.degrees(math.atan2(target_y - self.hitbox.centery, target_x - self.hitbox.centerx))
                    break

        else:
            direction = pygame.math.Vector2(self.finish[0] - self.start[0], self.finish[1] - self.start[1]).normalize()
            self.hitbox = self.hitbox.move(direction.x * self.speed, direction.y * self.speed)
            angle = math.degrees(math.atan2(self.finish[1] - self.hitbox.centery, self.finish[0] - self.hitbox.centerx))

        self.image = pygame.transform.rotate(self.base_image, -angle - 90)
        self.rect = self.image.get_rect(center=self.hitbox.center)




    def update(self, group_dict, world, current_time):

        player = group_dict['player_group'].sprites()[0]

        self.move()

        # Check if the enemy has reached the player's hitbox
        if self.rect.colliderect(player.rect):
            group_dict['player_group'].sprites()[0].health -= 30
        else:
            # Check if the enemy's health is 0 or less, and kill it
            if self.health <= 0:
                self.kill()


        if current_time >= self.neigh_time + self.neigh_cooldown:
            random.choice(self.neigh_sounds).play()
            self.neigh_time = current_time
            self.neigh_cooldown = random.randint(5, 15)


        self.draw_health_bar(self.hitbox.midtop, self.health, self.max_health)

