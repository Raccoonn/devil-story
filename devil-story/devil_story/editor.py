
## Standard Library
import sys
import math
import heapq
import random

## Third Party
import pygame
import networkx as nx

## Game modules
import tools





# pygame.event module
# https://www.pygame.org/docs/ref/event.html
#
# Making a clickable grid using Pygame
# https://stackoverflow.com/questions/73835007/making-a-clickable-grid-using-pygame/73835336#73835336
#
# GitHub - Grid
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_grid.md

import pygame

class Cell:
    def __init__(self):
        self.clicked = False

grid_size, cell_size = 40, 20
board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

pygame.init()
window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load('assets/images/grass.png').convert(), (800, 800))


draw_surf = pygame.Surface((800, 800), pygame.SRCALPHA)
draw_surf.fill(pygame.Color('#00000000'))

run = True
while run:
    
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:
                row = event.pos[1] // cell_size
                col = event.pos[0] // cell_size
                board[row][col].clicked = True


    

    # window.fill((255,255,255,128))

    for iy, rowOfCells in enumerate(board):
        for ix, cell in enumerate(rowOfCells):
            color = pygame.Color(64, 64, 64, 255) if cell.clicked else pygame.Color(164, 164, 164, 0)
            cell_rect = pygame.Rect(ix*cell_size+1, iy*cell_size+1, cell_size-2, cell_size-2)
            pygame.draw.rect(draw_surf, color, cell_rect)


    window.blit(background, (0, 0)) 

    window.blit(draw_surf, (0, 0))


    pygame.display.flip()

pygame.quit()
exit()