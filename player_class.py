import pygame
import settings as s

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = vec((self.grid_pos.x * self.app.cell_width)
                           + s.TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2,
                           (self.grid_pos.y * self.app.cell_height)
                           + s.TOP_BOTTOM_BUFFER//2 + self.app.cell_height//2)
        self.direction = vec(1, 0)

    def update(self):
        self.pix_pos += self.direction
        self.grid_pos[0] = (self.pix_pos[0]
                            - s.TOP_BOTTOM_BUFFER
                            + self.app.cell_width//2)//self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1]
                            - s.TOP_BOTTOM_BUFFER
                            + self.app.cell_height//2)//self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, s.PLAYER_COLOUR,
                           (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width//2 - 2)

        # draw grid
        pygame.draw.rect(self.app.screen, s.RED,
                         (self.grid_pos[0] * self.app.cell_width
                             + s.TOP_BOTTOM_BUFFER//2,
                          self.grid_pos[1] * self.app.cell_height
                             + s.TOP_BOTTOM_BUFFER//2,
                          self.app.cell_width, self.app.cell_height), 1)

    def move(self, direction):
        self.direction = direction
