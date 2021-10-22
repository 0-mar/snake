import random

import pygame
import data.states.state as state
import data.snake as snake
import data.barrier as barrier

import data.food.banana as banana
import data.food.hamburger as hamburger
import data.food.mushroom as mushroom

import data.camera as camera

import data.blocks.portal as portal

import os


MAP_WIDTH = 1024
MAP_HEIGHT = 1024


class GameState(state.State):
    def __init__(self, g, gamemode_number):
        state.State.__init__(self, g)

        # load images
        self.background_img = pygame.image.load("data/assets/background/game_background.png").convert()

        # load sounds
        self.eat_sound = pygame.mixer.Sound("data/assets/sounds/pochutina.mp3")
        self.hamburger_sound = pygame.mixer.Sound("data/assets/sounds/hamburger.mp3")

        # font
        self.score_font = pygame.font.SysFont("microsoftsansserif", 40)

        # colors
        self.black = (5, 5, 5)
        self.white = (255, 255, 255)

        self.green = (29, 220, 5)
        self.red = (200, 54, 5)
        self.violet = (77, 4, 145)

        self.game_over = False

        self.ui_width = MAP_WIDTH
        self.ui_height = MAP_HEIGHT

        # --------- game objects ---------
        self.snake = snake.Snake(((MAP_WIDTH // 2) // self.game.tile_size) * self.game.tile_size,
                                 ((MAP_HEIGHT // 2) // self.game.tile_size) * self.game.tile_size, self.game, self)
        self.cam = camera.Camera(self.game, self.snake)

        self.barriers = barrier.Barrier(self.game)

        """lst = []
        r = [1] * 24
        lst.append(r)

        self.barriers.create_barrier_chunk(336, 400, lst)
        self.barriers.create_barrier_chunk(336, MAP_HEIGHT - 400, lst)
        self.barriers.create_barrier_chunk(SCREEN_WIDTH // 2 - 6 * TILE_SIZE, SCREEN_HEIGHT - 320,
                                           [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]])"""

        banan_0_img = pygame.image.load("data/assets/food/banan_0.png").convert_alpha()
        banan_1_img = pygame.image.load("data/assets/food/banan_1.png").convert_alpha()
        banan_2_img = pygame.image.load("data/assets/food/banan_2.png").convert_alpha()
        self.banan_list = [banan_0_img, banan_1_img, banan_2_img]

        hamburger_0_img = pygame.image.load("data/assets/food/hamburger_0.png").convert_alpha()
        hamburger_1_img = pygame.image.load("data/assets/food/hamburger_1.png").convert_alpha()
        hamburger_2_img = pygame.image.load("data/assets/food/hamburger_2.png").convert_alpha()
        self.hamburger_list = [hamburger_0_img, hamburger_1_img, hamburger_2_img]

        mushroom_0_img = pygame.image.load("data/assets/food/mushroom_0.png").convert_alpha()
        self.mushroom_list = [mushroom_0_img]

        # stores all food instances
        self.food_list = []
        self.food_list = [banana.Banana(self.game, self, self.banan_list, self.eat_sound),
                          hamburger.Hamburger(self.game, self, self.hamburger_list, random.randint(5, 16), random.randint(0, 1), self.hamburger_sound),
                          mushroom.Mushroom(self.game, self, self.mushroom_list, self.eat_sound)]

        # stores all effects currently affecting the game
        self.effects_list = []

        self.portal_block = None

        self.score = 0

        self.gamemode = None
        self.gamemode_number = gamemode_number
        self.set_gamemode(gamemode_number)

    def draw_background(self, surface, offset_x, offset_y):
        # surface.fill(BLACK)
        surface.blit(self.background_img, (0 - offset_x, 0 - offset_y))

    def draw_score(self, surface):
        self.draw_text(surface, f"Skore: {self.score}", self.score_font, self.violet, 20, 20)

    def draw_text(self, surface, text, font, text_col, x, y):
        img = font.render(text, True, self.black)
        surface.blit(img, (x + 3, y + 3))
        img = font.render(text, True, text_col)
        surface.blit(img, (x, y))

    def update(self, time_passed):
        self.snake.update(time_passed)
        self.gamemode.update()

        for foodstuff in self.food_list:
            if foodstuff.active:
                foodstuff.update(time_passed)

        self.barriers.update()

        for effect in self.effects_list:
            effect.update()
            self.effects_list[:] = [effect for effect in self.effects_list if effect.active]

        if self.portal_block is not None:
            self.portal_block.update()

    def render(self, surface):
        self.cam.scroll_camera()
        self.draw_background(surface, self.cam.offset_x, self.cam.offset_y)

        self.snake.draw(surface, self.cam.offset_x, self.cam.offset_y)

        for foodstuff in self.food_list:
            if foodstuff.active:
                foodstuff.draw(surface, self.cam.offset_x, self.cam.offset_y)

        self.barriers.draw(surface, self.cam.offset_x, self.cam.offset_y)
        self.draw_score(surface)

        for effect in self.effects_list:
            effect.draw(surface)

        if self.portal_block is not None:
            self.portal_block.draw(surface, self.cam.offset_x, self.cam.offset_y)

    def reset_game(self):
        self.snake = snake.Snake(((MAP_WIDTH // 2) // self.game.tile_size) * self.game.tile_size,
                                 ((MAP_HEIGHT // 2) // self.game.tile_size) * self.game.tile_size, self.game, self)
        self.cam = camera.Camera(self.game, self.snake)

        self.food_list = []
        self.food_list = [banana.Banana(self.game, self, self.banan_list, self.eat_sound),
                          hamburger.Hamburger(self.game, self, self.hamburger_list, random.randint(5, 16),
                                              random.randint(0, 1), self.hamburger_sound),
                          mushroom.Mushroom(self.game, self, self.mushroom_list, self.eat_sound)]

        # stores all effects currently affecting the game
        self.effects_list = []

        self.portal_block = None

    def set_gamemode(self, gamemode_number):
        if gamemode_number == 0:
            self.gamemode = InfiniteGamemode(self)
        elif gamemode_number == 1:
            self.gamemode = LevelsGamemode(self)


class InfiniteGamemode:
    def __init__(self, game_world):
        self.game_world = game_world

    def update(self):
        pass


class LevelsGamemode(InfiniteGamemode):
    def __init__(self, game_world):
        super().__init__(game_world)
        self.level_number = 0
        self.score_required = 10
        self.score_threshold = self.score_required

        #self.game_world.barriers.load_from_file(f"data/level_data/{self.level_number}.txt")
        self.set_level(self.level_number)

    def update(self):
        if self.game_world.score >= self.score_threshold and self.game_world.portal_block is None and self.level_number != len(os.listdir("data/level_data")) - 1:
            # spawn portal to next level
            self.game_world.portal_block = portal.Portal(self.game_world)

    def set_level(self, level_number):
        if level_number < len(os.listdir("data/level_data")):
            self.score_threshold = self.score_required * (level_number + 1)
            self.level_number = level_number
            self.game_world.barriers = barrier.Barrier(self.game_world.game)
            self.game_world.barriers.load_from_file(f"data/level_data/{self.level_number}.txt")
            self.game_world.reset_game()


