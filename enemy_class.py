import pygame
import random
import settings as s
from timeit import default_timer as timer

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move:
                self.move()

        #setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0]
                            - s.TOP_BOTTOM_BUFFER
                            + self.app.cell_width//2)//self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1]
                            - s.TOP_BOTTOM_BUFFER
                            + self.app.cell_height//2)//self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.personality == "speedy":
            speed = 2
        elif self.personality == "random":
            speed = 1.5
        else:
            speed = 1
        return speed

    def set_target(self):
        if self.app.scared_enemies == 0:
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > s.COLS // 2 and self.app.player.grid_pos[1] > s.ROWS // 2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > s.COLS // 2 and self.app.player.grid_pos[1] < s.ROWS // 2:
                return vec(1, s.ROWS - 2)
            if self.app.player.grid_pos[0] < s.COLS // 2 and self.app.player.grid_pos[1] > s.ROWS // 2:
                return vec(s.COLS - 2, 1)
            else:
                return vec(s.COLS - 2, s.ROWS - 2)

    def time_to_move(self):
        if int(self.pix_pos.x+ s.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0) or self. direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+ s.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0) or self. direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width)
                           + s.TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2,
                           (self.grid_pos.y * self.app.cell_height)
                           + s.TOP_BOTTOM_BUFFER//2 + self.app.cell_height//2)

    def set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (148, 0, 211)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "scared"
