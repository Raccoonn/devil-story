
## Standard Library
import json
import sys
import math
import heapq
import random

## Third Party
import pygame
import matplotlib.pyplot as plt

## Game modules




def load_sprite_assets(name: str) -> dict:
    """Load given sprite assets from configuration file

    Parameters
    ----------
    name : str
        Sprite name

    Returns
    -------
    dict
        Dictionary of image and sound assets
    """
    with open(f'configs/{name}.json', 'r') as f:
        config = json.load(f)

    assets = {'images' : {}, 'sounds' : {}}         # type: dict

    for key, val in config['images'].items():
        image = pygame.image.load(f'assets/images/{val[0]}').convert_alpha()
        assets['images'][key] = pygame.transform.rotozoom(image, 0, val[1])

    for key, val in config['sounds'].items():
        sound = pygame.mixer.Sound(f'assets/sounds/{val[0]}')
        sound.set_volume(val[1])
        assets['sounds'][key] = sound

    return assets





def is_within_playable_area(position: pygame.math.Vector2, world) -> bool:
    """Boolean check if position is within playable area

    Parameters
    ----------
    position : tuple[int, int]
        (X, Y) coordinates of object to check

    Returns
    -------
    bool
        True if position within playable area - else False
    """

    for wall in world.walls:
        if wall.collidepoint(position):
            return False
        
    for fence in world.fences:
        if fence.collidepoint(position):
            return False
        
    return True

    left_square = pygame.Rect(45, 110, 260, 440)
    hallway = pygame.Rect(400, 200, 200, 100)
    right_square = pygame.Rect(480, 110, 260, 440)

    # if hallway.collidepoint(position):
    #     return False
    # else:
    #     return True

    return True


def create_playable_area_grid(height: int, width: int, offset: int, grid_size: int, world) -> list:
    """Create discretized grid for game area

    Parameters
    ----------
    grid_size : int
        Size of discretization

    Returns
    -------
    list
        List of bools indicating if grid position is within playable area
    """
    grid = []
    for y in range(0-offset, height+offset, grid_size):
        row = []
        for x in range(0-offset, width+offset, grid_size):
            pos = pygame.math.Vector2(x, y)
            is_obstacle = not is_within_playable_area(pos, world)
            row.append(is_obstacle)
        grid.append(row)

    return grid










