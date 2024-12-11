
## Standard Library
import sys
import math
import heapq
import random
import time

## Third Party
import pygame

## Game modules
import oldman
import tools






class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.display, playable_area_grid: list[list]) -> None:
        """Generic enemy object

        Parameters
        ----------
        screen : pygame.display
            Pygame screen
        playable_area_grid : list[list]
            Matrix of bools for playable area
        """
        super().__init__()

        self.screen = screen
        self.playable_area_grid = playable_area_grid


        self.next_loc = None


    def spawn_randomly(self, player_pos: pygame.math.Vector2, min_distance: int) -> None:
        """Spawn mummy at random location

        Parameters
        ----------
        playable_area_grid : list
            List of inbounds coordinates
        player_position : pygame.math.Vector2
            Player position as pygame vector
        min_distance : int
            Minimum distance from player to be spawned
        """
        if not self.spawned:
            x, y = self.get_random_position(self.playable_area_grid, self.grid_size)
            self.pos = pygame.math.Vector2(x, y)
            self.hitbox_rect = self.image.get_rect(center=self.pos)
            self.hitbox_rect.height = 40
            self.hitbox_rect.width = 40
            distance_to_player = pygame.math.Vector2(x - player_pos.x, y - player_pos.y).length()

            if distance_to_player >= min_distance:
                self.rect.topleft = (x, y)
                self.spawned = True  # Set the spawned flag to True


    def get_random_position(self, playable_area_grid: list, grid_size: int) -> tuple[int, int]:
        """Choose a random position within playable area

        Parameters
        ----------
        playable_area_grid : list
            List of inbounds coordinates
        grid_size : int
            Screen discretization 

        Returns
        -------
        tuple[int, int]
            Tuple of X, Y coorindates to spawn mummy
        """
        valid_positions = []
        for y in range(0, len(playable_area_grid) * grid_size, grid_size):
            for x in range(0, len(playable_area_grid[0]) * grid_size, grid_size):
                grid_x = int(x / grid_size)
                grid_y = int(y / grid_size)

                if 0 <= grid_x < len(playable_area_grid[0]) and 0 <= grid_y < len(playable_area_grid):
                    if not playable_area_grid[grid_y][grid_x]:
                        valid_positions.append((x, y))

        if valid_positions:
            return random.choice(valid_positions)
        else:
            # If no valid position is found, return a default position
            return 300, 300


    def update_path_to_target(self, target_pos: pygame.math.Vector2) -> None:
        """A* path algorithm

        Parameters
        ----------
        target_pos : pygame.math.Vector2
            Target position as pygame vector
        """
        start = (int(self.hitbox_rect.x / self.grid_size), int(self.hitbox_rect.y / self.grid_size))
        goal = (int(target_pos.x / self.grid_size), int(target_pos.y / self.grid_size))
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        open_set = []
        heapq.heappush(open_set, (0, start))
        cost_to_point = {start: 0}
        came_from = {start: None}

        while open_set:
            current_cost, current_point = heapq.heappop(open_set)

            if current_point == goal:
                # Reconstruct the path
                path = []
                while current_point:
                    path.append(current_point)
                    current_point = came_from[current_point]
                self.path = path[::-1]
                return

            for move in moves:
                new_point = (current_point[0] + move[0], current_point[1] + move[1])

                if (
                        0 <= new_point[0] < len(self.playable_area_grid[0])
                        and 0 <= new_point[1] < len(self.playable_area_grid)
                        and not self.playable_area_grid[new_point[1]][new_point[0]]
                ):
                    new_cost = cost_to_point[current_point] + 1
                    if (
                            new_point not in cost_to_point
                            or new_cost < cost_to_point[new_point]
                    ):
                        cost_to_point[new_point] = new_cost
                        priority = (new_cost + self.heuristic(new_point, goal), new_point)
                        heapq.heappush(open_set, priority)
                        came_from[new_point] = current_point

        self.path = []  # If no path is found, clear the existing path



    def move_towards_target_astar(self, target_pos: pygame.math.Vector2, world) -> None:
        """Update mummy current position using A* path

        Parameters
        ----------
        player : oldman.Oldman
            Player Oldman object
        """
        ## Update rotation
        if self.alive:

            ## Update position
            if self.path:
                for next_point in reversed(self.path):

                    target_x = next_point[0] * self.grid_size + self.grid_size / 2
                    target_y = next_point[1] * self.grid_size + self.grid_size / 2

                    try:
                        direction = pygame.math.Vector2(target_x - self.hitbox_rect.x, target_y - self.hitbox_rect.y).normalize()
                    except:
                        direction = pygame.math.Vector2(self.hitbox_rect.x, self.hitbox_rect.y).normalize()
                    
            


                    new_rect = self.hitbox_rect.move(direction.x * self.speed, direction.y * self.speed)

                    grid_x = int(new_rect.centerx / self.grid_size)
                    grid_y = int(new_rect.centery / self.grid_size)
                    

                    # previous_pos = self.pos

                    # self.pos.x += direction.x * self.speed
                    # self.pos.y += direction.y * self.speed

                    # self.hitbox_rect.center = self.pos

                    # if (0 <= self.pos.x < 800 and
                    #     0 <= self.pos.y < 800 and
                    #     self.hitbox_rect.collidelist(world.walls) < 0 and
                    #     self.hitbox_rect.collidelist(world.fences) < 0
                    #     ):
                    #     break  # Exit the loop if a valid position is found

                    # else:
                    #     self.pos = previous_pos
                    #     self.hitbox_rect.center = self.pos

                    if (
                            0 <= grid_x < len(self.playable_area_grid[0])
                            and 0 <= grid_y < len(self.playable_area_grid)
                            and not self.playable_area_grid[grid_y][grid_x]
                    ):
                        self.hitbox_rect = new_rect
                        self.pos = pygame.math.Vector2(new_rect.centerx, new_rect.centery)
                        break  # Exit the loop if a valid position is found



                angle = math.degrees(math.atan2(target_y - self.pos.y, target_x - self.pos.x))
                self.rotation_angle = -angle - 90
                self.image = pygame.transform.rotate(self.base_image, self.rotation_angle)
                self.rect = self.image.get_rect(center=self.hitbox_rect.center)










    def draw_health_bar(self) -> None:
        """Draw mummy health bar on game screen
        """
        ## Scale health and draw healthbar background
        health_ratio = self.health / self.max_health
        bar_width, bar_height = 40, 5
        health_bar_width = int(bar_width * health_ratio)
        health_bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(health_bar_surface, (255, 255, 255), (0, 0, bar_width, bar_height))

        ## Set color for current health percentage
        if health_ratio > 0.6:
            color = (0, 255, 0)  # Green
        elif health_ratio > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        ## Draw bar on enemy
        pygame.draw.rect(health_bar_surface, color, (0, 0, health_bar_width, bar_height))
        health_bar_pos = (self.rect.centerx - bar_width // 2, self.rect.y - 10)
        self.screen.blit(health_bar_surface, health_bar_pos)







