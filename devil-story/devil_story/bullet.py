
## Standard Library
import sys
import math
import heapq
import random

## Third Party
import pygame

## Game modules
import tools



class Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 bullet_assets: dict,
                 x: int, y: int, bullet_angle: float,
                 screen: pygame.display, playable_area_grid: list[list]
                 ) -> None:
        """Bullet object

        Parameters
        ----------
        bullet_assets : dict
            Bullet image and sound assets
        x : int
            X spawn coordinate
        y : int
            Y spawn coordinate
        bullet_angle : float
            Spawn angle
        screen : pygame.display
            Pygame screen
        playable_area_grid : list[list]
            Matrix of bools for playable area
        """        
        super().__init__()
        ## Assets
        self.image = bullet_assets['images']['bullet']

        self.shooting_sounds = [v for k,v in bullet_assets['sounds'].items() if 'shoot' in k]
        self.reload_sound = bullet_assets['sounds']['reload']

        ## Stats
        self.damage = 30
        self.speed = 30
        self.bullet_angle = bullet_angle - 90
        self.x = x
        self.y = y
        self.dx = math.cos(self.bullet_angle * (2 * math.pi / 360)) * self.speed
        self.dy = math.sin(self.bullet_angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = 750
        self.spawn_time = pygame.time.get_ticks()

        ## Display
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.playable_area_grid = playable_area_grid

        ## Play shooting and reload sounds
        random.choice(self.shooting_sounds).play()
        self.reload_sound.play()



    def update(self, group_dict, world, current_time) -> None:
        """Move bullet

        Parameters
        ----------
        enemy_group : pygame.sprite.Group
            Pygame group of enemy sprites
        """
        self.x += self.dx
        self.y += self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        ## Check bullet status for time, enemy hit, leaving play area
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

        enemy_hit = pygame.sprite.spritecollide(self, group_dict['enemy_group'], False)
        for enemy in enemy_hit:
            enemy.health -= self.damage
            self.kill()

        self.object = pygame.Rect(400, 200, 200, 100)

        if (not (0 < self.rect.x <= 800) or
            not (0 < self.rect.y <= 800) or
            self.rect.collidelist(world.walls) >= 0
            ):
            self.kill()







