import data.effects.effect as effect
import data.food.mushroom
import pygame
import data.animation


class DoubleScoreEffect(effect.Effect):
    def __init__(self, duration, game_state):
        super().__init__(duration, game_state)

        self.duration *= 2

        # load images
        self.glow_0_img = pygame.image.load("data/assets/glow/glow_0.png").convert_alpha()
        self.glow_1_img = pygame.image.load("data/assets/glow/glow_1.png").convert_alpha()
        self.glow_2_img = pygame.image.load("data/assets/glow/glow_2.png").convert_alpha()

        self.animation = data.animation.Animation([self.glow_0_img, self.glow_1_img, self.glow_2_img], 3, self.game_state.game)

        self.glow_rect = self.glow_0_img.get_rect()

        for food in self.game_state.food_list:
            food.multiplier = 2

    def draw(self, surface):
        self.game_state.draw_text(surface, "Dvojite skore", self.effect_font, self.white, self.game_state.game.screen_width - 250, 20)

        for food in self.game_state.food_list:
            if food.active and type(food) != data.food.mushroom.Mushroom:
                rect = self.glow_rect.copy()
                rect.center = food.rect.center
                surface.blit(self.animation.current_image, (rect.x - self.cam.offset_x, rect.y - self.cam.offset_y))

    def update(self):
        super(DoubleScoreEffect, self).update()

        self.animation.update()

    def on_effect_disable(self):
        for food in self.game_state.food_list:
            food.multiplier = 1



