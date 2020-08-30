import pygame
import sys
import copy
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
        self.cell_width = s.MAZE_WIDTH//s.COLS
        self.cell_height = s.MAZE_HEIGHT//s.ROWS
        self.walls = []
        self.coins = []
        self.bonus = []
        self.scared_enemies = 0
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = p.Player(self, vec(self.p_pos))
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
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_draw()
            elif self.state == 'game won':
                self.game_won_events()
                self.game_won_draw()
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
                    elif char == "H":
                        self.bonus.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2","3","4","5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

        self.enemies.remove(self.enemies[3])



    def draw_grid(self):
        for x in range(s.WIDTH//self.cell_width):
            pygame.draw.line(self.background, s.GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, s.HEIGHT))
        for y in range(s.HEIGHT//self.cell_height):
            pygame.draw.line(self.background, s.GREY,
                             (0, y * self.cell_height),
                             (s.WIDTH, y * self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        self.enemies = []
        self.make_enemies()
        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(xidx, yidx))
        self.state = "play"

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
        if self.scared_enemies > 0:
            self.scared_enemies -= 1
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos and self.scared_enemies == 0:
                self.remove_life()
            elif enemy.grid_pos == self.player.grid_pos and self.scared_enemies != 0:
                self.remove_enemy(enemy)

    def play_draw(self):
        self.screen.fill(s.BLACK)
        self.screen.blit(self.background,
                         (s.TOP_BOTTOM_BUFFER//2, s.TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                        self.screen, [230, 0], s.START_TEXT_SIZE, s.WHITE, s.START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def remove_enemy(self, to_eat):
        self.enemies.remove(to_eat)
        self.player.current_score += 150
        if not self.enemies:
            self.state = "game won"

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
            (int(coin.x*self.cell_width)+self.cell_width//2+ s.TOP_BOTTOM_BUFFER//2,
             int(coin.y*self.cell_height)+self.cell_height//2+ s.TOP_BOTTOM_BUFFER//2), 5)
            for plus in self.bonus:
                pygame.draw.circle(self.screen, (0, 100, 10),
                (int(plus.x*self.cell_width)+self.cell_width//2+ s.TOP_BOTTOM_BUFFER//2,
                 int(plus.y*self.cell_height)+self.cell_height//2+ s.TOP_BOTTOM_BUFFER//2), 10)

# GAME OVER

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_draw(self):
        self.screen.fill(s.BLACK)
        quit_text = "Press the ESC key to quit"
        again_text = "Press SPACE bar to play again"
        self.draw_text("GAME OVER", self.screen, [s.WIDTH//2, 100], 52, s.RED, "arial", centered = True)
        self.draw_text(str(self.player.current_score), self.screen, [s.WIDTH//2, 200], 82, s.RED, "arial", centered = True)
        self.draw_text(again_text, self.screen, [s.WIDTH//2, s.HEIGHT//2], 36, (190, 190, 190), "arial", centered = True)
        self.draw_text(quit_text, self.screen, [s.WIDTH//2, s.HEIGHT//1.5], 36, (190, 190, 190), "arial", centered = True)
        pygame.display.update()


# GAME WON

    def game_won_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_won_draw(self):
        self.screen.fill(s.BLACK)
        quit_text = "Press the ESC key to quit"
        again_text = "Press SPACE bar to play again"
        self.draw_text("WINNER", self.screen, [s.WIDTH//2, 100], 52, s.RED, "arial", centered = True)
        self.draw_text(str(self.player.current_score), self.screen, [s.WIDTH//2, 200], 82, s.RED, "arial", centered = True)
        self.draw_text(again_text, self.screen, [s.WIDTH//2, s.HEIGHT//2], 36, (190, 190, 190), "arial", centered = True)
        self.draw_text(quit_text, self.screen, [s.WIDTH//2, s.HEIGHT//1.5], 36, (190, 190, 190), "arial", centered = True)
        pygame.display.update()
