
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame

## Game modules
from bottle import Bottle
from bullet import Bullet
from horse  import Horse
from mummy  import Mummy
from oldman import Oldman
from level import Level

import tools





def start_menu() -> None:
    """Display start menu

    Returns
    -------
    None
        Return used to end function and begin gameplay loop
    """
    menu_font = pygame.font.Font(None, 48)
    menu_text = menu_font.render('Press "Space" to Start', True, (255, 255, 255))
    text_rect = menu_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    pygame.mixer.Channel(0).play(start_menu_sound, loops=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Stop the start menu sound when the space key is pressed
                pygame.mixer.Channel(0).stop()
                pygame.mixer.Channel(1).play(background_music, loops=-1)
                return  # Exit the start menu if the space key is pressed

        screen.blit(background, (0, 0))
        screen.blit(menu_text, text_rect)
        pygame.display.update()



def game_over_screen(message: str) -> None:
    """Display game over screen

    Parameters
    ----------
    message : str
        Message displayed at game over

    Returns
    -------
    bool
        True if player selects another game - else False (Quit)
    """
    screen.blit(background, (0, 0))  # Display the background map

    # Display you died mssg
    font = pygame.font.Font(None, 48)
    game_over_text = font.render(f'{message}', True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(game_over_text, text_rect)

    # Display retry message
    retry_font = pygame.font.Font(None, 30)
    retry_text = retry_font.render('Press Space to Retry', True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    screen.blit(retry_text, retry_rect)

    pygame.display.update()
    pygame.mixer.Channel(1).stop()
    pygame.mixer.Channel(0).play(start_menu_sound, loops=-1)

    # Wait for the player to press space to retry
    space_pressed = False
    while not space_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True

    # Kill all enemies before retrying
    for enemy in enemy_group.sprites():
        enemy.kill()

    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(1).play(background_music, loops=-1)
    return True  # Retry the gamew







if __name__ == '__main__':


    pygame.init()

    height, width = 800, 800

    

    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption('Devil Story')
    clock = pygame.time.Clock()

    
    ## Load background and calculate playable area grid
    background = pygame.transform.scale(pygame.image.load('assets/images/grass.png').convert(), (height, width))




    # Load the sound for start menu and retry menu on channel 1
    background_music = pygame.mixer.Sound('assets/sounds/Action 1.mp3')
    pygame.mixer.Channel(1).set_volume(0)
    pygame.mixer.Channel(1).play(background_music, -1)
    pygame.mixer.Channel(1).stop()

    # Load the sound for start menu and retry menu on channel 1
    start_menu_sound = pygame.mixer.Sound('assets/sounds/Ambient 2.mp3')
    pygame.mixer.Channel(1).set_volume(0)
    pygame.mixer.Channel(0).play(start_menu_sound, -1)
    pygame.mixer.Channel(1).stop()



    ## Load assetsw
    bottle_assets = tools.load_sprite_assets('bottle')
    bullet_assets = tools.load_sprite_assets('bullet')
    horse_assets  = tools.load_sprite_assets('horse')
    mummy_assets  = tools.load_sprite_assets('mummy')
    oldman_assets = tools.load_sprite_assets('oldman')
    world_assets  = tools.load_sprite_assets('world')

    world = Level(world_assets)

    grid_size = 20
    playable_area_grid = tools.create_playable_area_grid(height, width, 0, grid_size, world)

    # print(playable_area_grid)

    horse_playable_area_grid = tools.create_playable_area_grid(height, width, 0, grid_size, world)

    ## Main loop
    running, restart = True, True

    while running:

        ## Timestamp of frame
        current_time = time.time()

        ## Clear last screen with blank
        screen.blit(background, (0, 0))
        
        for wall in world.walls:
            screen.blit(world.wall_image, wall)

        for fence in world.fences:
            screen.blit(world.fence_image, fence)


        ## Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        ## Initialize entities
        if restart:

            ## Create groups
            all_sprites_group = pygame.sprite.Group()
            item_group = pygame.sprite.Group()
            bullet_group = pygame.sprite.Group()
            enemy_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()

            group_dict = {
                          'all_sprites_group' : all_sprites_group,
                          'item_group' : item_group,
                          'bullet_group' : bullet_group,
                          'enemy_group' : enemy_group,
                          'player_group' : player_group
                         }

            # Create game entities
            player = Oldman(oldman_assets, bullet_assets, screen, playable_area_grid, grid_size)
            player_group.add(player)

            horse = Horse(horse_assets, screen, horse_playable_area_grid, grid_size)
            enemy_group.add(horse)

            bottle = Bottle(bottle_assets, screen, playable_area_grid)
            bottle_spawn_time = time.time()
            bottle_respawn = random.randint(10, 20)
            item_group.add(bottle)
 
            mummy = Mummy(mummy_assets, screen, playable_area_grid, grid_size)
            enemy_group.add(mummy)
 

            all_sprites_group.add(*[player, horse, bottle, mummy])






            start_menu()

            restart = False


        ## Handle bottle respawn
        if not item_group and current_time >= bottle_spawn_time + bottle_respawn:
            bottle = Bottle(bottle_assets, screen, playable_area_grid)
            bottle_spawn_time = time.time()
            bottle_respawn = random.randint(10, 20)
            all_sprites_group.add(bottle)
            item_group.add(bottle)
        if item_group:
            bottle_spawn_time = current_time


        ## Render and update all sprites




        all_sprites_group.draw(screen) 
        all_sprites_group.update(group_dict, world, current_time)


        


        ## Handle win/loss/restart
        if player.health <= 0 or horse.health <= 0:
            if player.health <= 0:
                message = 'You Died'
            else:
                message = 'You Win - The horse is dead'

            if game_over_screen(f'{message}'):
                restart = True
            else:
                running = False
            
            all_sprites_group.empty()



        pygame.display.update()
        clock.tick(60)


    pygame.quit()














