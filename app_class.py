import pygame
import sys
import settings as s
import player_class as p
from enemy_class import *
from settings import *


pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start screen'
        self.cell_width = s.MAZE_WIDTH//28
        self.cell_height = s.MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = p.Player(self, self.p_pos)
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start screen':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'play':
                self.play_events()
                self.play_update()
                self.play_draw()
            else:
                self.running = False
            self.clock.tick(s.FPS)
        pygame.quit()
        sys.exit()

# HELPERS

    def draw_text(self, message, screen, pos, size, colour,
                  font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(message, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(
            self.background, (s.MAZE_WIDTH, s.MAZE_HEIGHT))

        # open walls file;create walls list with co-ords of walls
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = vec(xidx, yidx)
                    elif char in ["2","3","4","5"]:
                        self.e_pos.append(vec(xidx, yidx))
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))



    def draw_grid(self):
        for x in range(s.WIDTH//self.cell_width):
            pygame.draw.line(self.background, s.GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, s.HEIGHT))
        for y in range(s.HEIGHT//self.cell_height):
            pygame.draw.line(self.background, s.GREY,
                             (0, y * self.cell_height),
                             (s.WIDTH, y * self.cell_height))

# INTRO

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'play'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(s.BLACK)
        self.draw_text('PRESS SPACE', self.screen, [s.WIDTH//2, s.HEIGHT//2],
                       s.START_TEXT_SIZE, (170, 132, 58), s.START_FONT,
                       centered=True)
        self.draw_text('HIGH SCORE', self.screen, [4, 0],
                       s.START_TEXT_SIZE, s.WHITE, s.START_FONT)
        pygame.display.update()

# PLAY SCREEN

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def play_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def play_draw(self):
        self.screen.fill(s.BLACK)
        self.screen.blit(self.background,
                         (s.TOP_BOTTOM_BUFFER//2, s.TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text('HIGH SCORE: 0', self.screen, [s.WIDTH//2 + 60, 0],
                       s.START_TEXT_SIZE, s.WHITE, s.START_FONT)
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                        self.screen, [100, 0], s.START_TEXT_SIZE, s.WHITE, s.START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        # self.coins.pop()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
            (int(coin.x*self.cell_width)+self.cell_width//2+ s.TOP_BOTTOM_BUFFER//2,
             int(coin.y*self.cell_height)+self.cell_height//2+ s.TOP_BOTTOM_BUFFER//2), 5)
