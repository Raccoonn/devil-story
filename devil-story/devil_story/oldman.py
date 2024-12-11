
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame

## Game modules
from bullet import Bullet
import tools


class Oldman(pygame.sprite.Sprite):
    def __init__(self, oldman_assets: dict, bullet_assets: dict, screen: pygame.display, playable_area_grid: list[list], grid_size) -> None:
        """Player character object

        Parameters
        ----------
        oldman_assets : dict
            Oldman image and sound assets
        bullet_assets : dict
            Bullet image and sound assets
        screen : pygame.display
            Pygame screen
        playable_area_grid : list[list]
            Matrix of bools for playable area
        """        
        super().__init__()
        ## Assets
        self.image = oldman_assets['images']['oldman']
        self.base_player_image = self.image
        self.bullet_assets = bullet_assets

        self.voice_sounds = [v for k,v in oldman_assets['sounds'].items() if 'voice' in k]

        ## Stats
        self.bullet_group = pygame.sprite.Group()
        self.pos = pygame.math.Vector2(200, 500)

        self.health = 10000
        self.max_health = 10000

        self.shooting = False
        self.powershot = False
        self.shooting_cooldown = 0.8
        self.shooting_time = 0

        self.booze = 0
        self.max_booze = 1
        self.bottles = 0
        self.drinking = False
        self.drinking_time = 0
        self.drinking_cooldown = 2

        self.voice_time = 0
        self.voice_cooldown = random.randint(5, 15)


        ## Display
        self.screen = screen
        self.hitbox_rect = self.image.get_rect(center=self.pos)
        self.hitbox_rect.height = 20
        self.hitbox_rect.width = 20

        self.rect = self.hitbox_rect.copy()
        self.gun_barrel_offset = pygame.math.Vector2(2, -40)
        self.playable_area_grid = playable_area_grid
        self.grid_size = grid_size

        self.object = pygame.Rect(400, 200, 200, 100)

        ## Cheats
        self.invuln = False


    def user_input(self, all_sprites_group: pygame.sprite.Group, world, current_time: float) -> None:
        """Update position attributes and handle shooting input

        Parameters
        ----------
        all_sprites_group : pygame.sprite.Group
            Pygame group of all current sprites
        current_time : float
            Time of frame
        """
        
        
        keys = pygame.key.get_pressed()


        previous_x, previous_y = self.pos

        ## Check valid position in X direction
        if keys[pygame.K_d]:
            self.pos.x += 3
        if keys[pygame.K_a]:
            self.pos.x += -3

        self.hitbox_rect.center = self.pos

        if (not 0 <= self.pos.x < 800 or 
            self.hitbox_rect.collidelist(world.walls) >= 0 or
            self.hitbox_rect.collidelist(world.fences) >= 0
            ):
            self.pos.x = previous_x


        ## Check valid position in Y direction
        if keys[pygame.K_s]:
            self.pos.y += 3
        if keys[pygame.K_w]:
            self.pos.y += -3

        self.hitbox_rect.center = self.pos

        if (not 0 <= self.pos.y < 800 or 
            self.hitbox_rect.collidelist(world.walls) >= 0 or
            self.hitbox_rect.collidelist(world.fences) >= 0
            ):
            self.pos.y = previous_y


        ## Update hitbox and rect
        self.hitbox_rect.center = self.pos


        ## Update rotation
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
        # ADDED 90 TO FIX CALCULATION FOR THE TIME BEING
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)) + 90
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)    
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)



        ## Consuming bottle
        if self.bottles > 0 and keys[pygame.K_SPACE] and not self.drinking:
            self.drinking = True
            self.drinking_time = current_time
            self.booze += 1
            self.bottles -= 1
            if self.booze == self.max_booze:
                self.powershot = True
                self.booze = 0

        ## Normal shot
        if pygame.mouse.get_pressed() == (1, 0, 0) and not self.shooting:
            self.shooting = True
            self.shooting_time = current_time
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            bullet = Bullet(self.bullet_assets, 
                            spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle,
                            self.screen, self.playable_area_grid)
            self.bullet_group.add(bullet)
            all_sprites_group.add(bullet)

        ## Power shot
        elif pygame.mouse.get_pressed() == (0, 0, 1) and not self.shooting and self.powershot:
            self.shooting = True
            self.powershot = False
            self.shooting_time = current_time
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            for theta in [-7.5, -3.25, 0, 3.25, 7.5]:
                bullet = Bullet(self.bullet_assets, 
                                spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle + theta,
                                self.screen, self.playable_area_grid)
                self.bullet_group.add(bullet)
                all_sprites_group.add(bullet)


        ## Cheats
        if keys[pygame.K_i]:
            if self.invuln:
                self.invuln = False
            else:
                self.invuln = True

        if self.invuln:
            self.health = 100









    def draw_health_info(self) -> None:
        """Draw Oldman object healthbar

        Parameters
        ----------
        screen : pygame.display
            Pygame screen
        """
        ## Draw text
        font = pygame.font.Font(None, 30)
        health_text = font.render('Health:', True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(150, 15))
        self.screen.blit(health_text, text_rect)

        ## Draw bar
        health_ratio = self.health / self.max_health
        bar_width, bar_height = 100, 10
        health_bar_width = int(bar_width * health_ratio)
        health_bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(health_bar_surface, (255, 255, 255), (0, 0, bar_width, bar_height))
        pygame.draw.rect(health_bar_surface, (255, 0, 0), (0, 0, health_bar_width, bar_height))
        health_bar_pos = (200, 10)
        self.screen.blit(health_bar_surface, health_bar_pos)


    def draw_booze_info(self) -> None:
        """Draw Oldman object boozebar

        Parameters
        ----------
        screen : pygame.display
            Pygame screen
        """
        ## Draw text
        font = pygame.font.Font(None, 30)
        booze_text = font.render('Booze:', True, (255, 255, 255))
        booze_text_rect = booze_text.get_rect(center=(500, 15))
        self.screen.blit(booze_text, booze_text_rect)

        ## Draw bar
        booze_ratio = self.booze / self.max_booze
        bar_width, bar_height = 100, 10
        booze_bar_width = int(bar_width * booze_ratio)
        booze_bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(booze_bar_surface, (255, 255, 255), (0, 0, bar_width, bar_height))
        pygame.draw.rect(booze_bar_surface, (0, 0, 255), (0, 0, booze_bar_width, bar_height))
        booze_bar_pos = (550, 10)
        self.screen.blit(booze_bar_surface, booze_bar_pos)


    def update(self, group_dict, world, current_time) -> None:
        """General update method for player object

        Parameters
        ----------
        all_sprites_group : pygame.sprite.Group
            Pygame group of all sprints
        bullet_group : pygame.sprite.Group
            Pygame group of bullet sprites
        """
        if not self.drinking:
            self.user_input(group_dict['all_sprites_group'], world, current_time)
            # self.move()

        ## Update player
        if self.drinking and current_time >= self.drinking_time + self.drinking_cooldown:
            self.drinking = False
        if self.shooting and current_time >= self.shooting_time + self.shooting_cooldown:
            self.shooting = False

        if current_time >= self.voice_time + self.voice_cooldown:
            random.choice(self.voice_sounds).play()
            self.voice_time = current_time
            self.voice_cooldown = random.randint(5, 15)

        self.draw_health_info()
        self.draw_booze_info()











