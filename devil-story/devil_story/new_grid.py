
## Standard Library


## Third Party
import pygame
import networkx as nx
from matplotlib import pyplot as plt

## Game modules
from level import Level

import tools



pygame.init()

height, width = 800, 800



screen = pygame.display.set_mode((height, width))
pygame.display.set_caption('Devil Story')
clock = pygame.time.Clock()


## Load background and calculate playable area grid
background = pygame.transform.scale(pygame.image.load('assets/images/grass.png').convert(), (height, width))





grid_size = 20



G = nx.grid_2d_graph(width // grid_size, height // grid_size)




# plt.show()

node_attr = {}

for row, y in enumerate(range(0, width, grid_size)):
    for col, x in enumerate(range(0, height, grid_size)):
        node_attr[(row, col)] = {'coords': (x + grid_size // 2, y + grid_size // 2)}

nx.set_node_attributes(G, node_attr)







world_assets  = tools.load_sprite_assets('world')

world = Level(width, height, grid_size, world_assets)




for node in list(G.nodes()):

    for obj in world.objects:
        if obj.collidepoint(G.nodes[node]['coords']):
            G.remove_node(node)
            break
    



plt.figure(figsize=(8,8))
pos = {(x,y):(y,-x) for x,y in G.nodes()}
nx.draw(G, pos=pos, 
        node_color='lightgreen', 
        with_labels=False,
        node_size=50)

# plt.show()



a = [[False] * (width // grid_size) for _ in  range(height // grid_size)]



for node in G.nodes():

    a[node[0]][node[1]] = True


print(a)

new_playable_grid = a


pos = {(x,y):(y,-x) for x,y in G.nodes()}
nx.draw(G, pos=pos, 
        node_color='lightgreen', 
        with_labels=False,
        node_size=50)

# plt.show()



pos_1 = (0 // grid_size, 0 // grid_size)

pos_2 = (798 // grid_size, 666 // grid_size)


print(pos_1, pos_2)

path = [G.nodes[node]['coords'] for node in nx.shortest_path(G, pos_1, pos_2)]

print(path)





for node in list(G.nodes):
    if node not in path:
        G.remove_node(node)



# plt.figure(figsize=(8,8))
pos = {(x,y):(y,-x) for x,y in G.nodes()}
nx.draw(G, pos=pos, 
        node_color='red', 
        with_labels=False,
        node_size=50)

# plt.show()



pygame.quit()



