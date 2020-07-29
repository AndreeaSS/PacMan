import pygame
import sys
import settings as s
import player_class as p


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
        self.player = p.Player(self, s.PLAYER_START_POS)

        self.load()

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

    def play_draw(self):
        self.screen.fill(s.BLACK)
        self.screen.blit(self.background,
                         (s.TOP_BOTTOM_BUFFER//2, s.TOP_BOTTOM_BUFFER//2))
        self.draw_grid()
        self.draw_text('HIGH SCORE: 0', self.screen, [s.WIDTH//2 + 60, 0],
                       s.START_TEXT_SIZE, s.WHITE, s.START_FONT)
        self.draw_text('CURRENT SCORE: 0', self.screen, [100, 0],
                       s.START_TEXT_SIZE, s.WHITE, s.START_FONT)
        self.player.draw()
        pygame.display.update()
