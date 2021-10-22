import data.effects.effect as effect
import pygame


class ShrinkSnakeEffect(effect.Effect):
    def __init__(self, duration, game_state, mushroom_rect_x, mushroom_rect_y):
        super(ShrinkSnakeEffect, self).__init__(duration, game_state)

        self.snake = self.game_state.snake

        self.mushroom_rect_x = mushroom_rect_x
        self.mushroom_rect_y = mushroom_rect_y

        if len(self.snake.segments) > 5:
            self.snake.segments.pop()
            self.snake.segments.pop()
            self.snake.segments.pop()
        else:
            self.active = False

        self.steps = 15
        self.steps_counter = 0

        self.timer = 2
        self.counter = 0

    def update(self):
        super(ShrinkSnakeEffect, self).update()

        self.counter += 1
        if self.counter >= self.timer:
            self.counter = 0
            self.steps_counter += 1
            if self.steps_counter >= self.steps:
                self.active = False

    def draw(self, surface):
        self.game_state.draw_text(surface, "-3 segmenty", self.effect_font, self.white, self.mushroom_rect_x - 100, self.mushroom_rect_y - 50 - (self.steps_counter * 2))