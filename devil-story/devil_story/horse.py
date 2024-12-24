
## Standard Library
import sys
import math
import heapq
import random

## Third Party
import pygame

## Game modules
import enemy
import oldman
import tools





class Horse(enemy.Enemy):
    def __init__(self, horse_assets: dict, screen: pygame.display, playable_area_grid: list[list], grid_size) -> None:
        """Horse enemy object

        Parameters
        ----------
        horse_assets : dict
            Horse image and sound assets
        screen : pygame.display
            Pygame screen
        playable_area_grid : list[list]
            Matrix of bools for playable area
        """
        super().__init__(screen, playable_area_grid)
        ## Assets
        self.image = horse_assets['images']['horse']
        self.base_image = self.image.copy()  # Store the original rotated image

        self.neigh_sounds = [v for k,v in horse_assets['sounds'].items() if 'neigh' in k]

        self.neigh_time = 0
        self.neigh_cooldown = random.randint(5, 15)

        ## Stats
        self.alive = True
        self.speed = 3
        self.spawned = False  # Flag to check if the enemy has been spawned
        self.rotation_angle = 0  # Initial rotation angle
        self.health = 500
        self.max_health = 500
        self.rest = 0
        self.show = True

        self.path = []  # Store the path calculated by A*
        self.path_update_timer = 0  # Timer to control path updates

        ## Display
        self.screen = screen
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.base_image.get_rect(center=self.rect.center)
        self.hitbox_rect.height = 15
        self.hitbox_rect.width = 15
        self.playable_area_grid = playable_area_grid
        self.grid_size = grid_size

        ## Spawn horse
        self.get_path()





    def heuristic(self, a, b):
        # heuristic using Euclidean distance
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    



    def get_path(self) -> None:
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
        self.rotation_angle = -angle - 90
        self.image = pygame.transform.rotate(self.base_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox_rect.center = self.rect.center  # Recalculate hitbox_rect position
        self.hitbox_rect.height = 10
        self.hitbox_rect.width = 10
        self.direction = pygame.math.Vector2(self.finish[0] - self.start[0], self.finish[1] - self.start[1]).normalize()

        self.rect.center = self.start



    def update(self, group_dict: dict, world, current_time: float) -> None:
        """Update horse object each frame

        Parameters
        ----------
        group_dict : dict
            Dictionary of all sprite groups
        current_time : float
            Time of frame
        """
        if (self.finish.distance_to(self.rect.center) < 200 or 
            not -300 < self.hitbox_rect.centerx < 1200 or
            not -300 < self.hitbox_rect.centery < 1200
            ):
            self.get_path()
            self.path = []
            self.path_update_timer = 0



        if 100 < self.hitbox_rect.centerx < 700 and 100 < self.hitbox_rect.centery < 700:

            if self.finish[0] < 1:
                tar_x = 1
            elif self.finish[0] > 799:
                tar_x = 799
            else:
                tar_x = self.finish[0]

            if self.finish[1] < 1:
                tar_y = 1
            elif self.finish[1] > 799:
                tar_y = 799
            else:
                tar_y = self.finish[1]

            local_target = pygame.math.Vector2((tar_x, tar_y))

            if self.path_update_timer <= 0 or not self.path:
                self.update_path_to_target(local_target)
                self.path_update_timer = 10
            else:
                self.path_update_timer -= 1

            self.move_towards_target_astar(local_target, world)

        else:
            self.direction = pygame.math.Vector2(self.finish[0] - self.start[0], self.finish[1] - self.start[1]).normalize()
            new_pos = self.pos + pygame.math.Vector2(self.direction.x * self.speed, self.direction.y * self.speed)
            self.pos = new_pos
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center



        # Check if the enemy has reached the player's hitbox
        if self.rect.colliderect(group_dict['player_group'].sprites()[0].rect):
            group_dict['player_group'].sprites()[0].health -= 30
        else:
            # Check if the enemy's health is 0 or less, and kill it
            if self.health <= 0:
                self.kill()


        if current_time >= self.neigh_time + self.neigh_cooldown:
            random.choice(self.neigh_sounds).play()
            self.neigh_time = current_time
            self.neigh_cooldown = random.randint(5, 15)


        self.draw_health_bar()



