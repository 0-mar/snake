import pygame

import data.states.main_menu
import data.states.game_state

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)


class Game:

    def __init__(self):
        # game variables
        self.screen_width = 1024
        self.screen_height = 1024
        self.tile_size = 16
        self.running = False

        self.fps = 15

        # colors
        self.black = (5, 5, 5)
        self.white = (255, 255, 255)

        self.green = (29, 220, 5)
        self.red = (200, 54, 5)
        self.violet = (77, 4, 145)

        self.scale = 1

        self.clock = pygame.time.Clock()

        self.monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Snake")

        self.last_key_pressed = None

        # stack for storing all of the states
        self.state_stack = []

        self.run_game()

    def update(self, time_passed):
        self.state_stack[-1].update(time_passed)

    def render(self):
        self.state_stack[-1].render(self.screen)
        # Render current state to the screen
        pygame.display.update()

    def run_game(self):
        main_menu = data.states.main_menu.MainMenu(self)
        main_menu.enter_state()

        self.on_resize_window(self.monitor_size[0], self.monitor_size[1])
        self.running = True

        while self.running:
            time_passed = self.clock.tick(self.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    self.on_resize_window(event.w, event.h)

                elif event.type == pygame.KEYDOWN:
                    self.last_key_pressed = event.key

            self.update(time_passed)
            self.render()

        pygame.quit()

    def on_resize_window(self, width, height):

        if width < 512:
            width = 512
        elif width >= 1024:
            width = 1024

        if height < 512:
            height = 512
        elif height >= 1024:
            height = 1024

        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.state_stack[-1].resize(width, height)
        #print(f"Momentalní scale: {self.state_stack[-1].scale}| rozmery okna: {width} x {height}| rozmery gui: {self.state_stack[-1].ui_width} x {self.state_stack[-1].ui_height}")

g = Game()
