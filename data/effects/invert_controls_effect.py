import data.effects.effect as effect
import pygame
import random


class InvertControlsEffect(effect.Effect):
    def __init__(self, duration, game_state):
        super().__init__(duration, game_state)

        self.original_controls = self.game_state.snake.controls
        self.inverted_controls = self.original_controls.copy()

        self.inverted_controls["up"], self.inverted_controls["down"] = self.inverted_controls["down"], self.inverted_controls["up"]
        self.inverted_controls["left"], self.inverted_controls["right"] = self.inverted_controls["right"], self.inverted_controls["left"]

        self.game_state.snake.controls = self.inverted_controls

        self.offset_x = 0
        self.offset_y = 0

        self.effect_surf = pygame.Surface((self.game_state.game.screen_width, self.game_state.game.screen_height), pygame.SRCALPHA).convert_alpha()
        self.effect_surf.set_alpha(80)
        self.create_polygons(self.game_state.game.screen_width, self.game_state.game.screen_height)

        #self.effect_surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100))
        self.effect_surf_rect = self.effect_surf.get_rect()

    def draw(self, surface):
        surface.blit(self.effect_surf, self.effect_surf_rect)
        self.game_state.draw_text(surface, "Invertovane ovladani", self.effect_font, self.white, self.game_state.game.screen_width - 380 + self.offset_x, 20 + self.offset_y)

    def update(self):
        super().update()

        if self.duration_counter % 2 == 0:
            self.offset_y = random.randint(-2, 2)
            self.offset_x = random.randint(-2, 2)

    def on_effect_disable(self):
        self.game_state.snake.controls = self.original_controls

    def create_polygons(self, screen_width, screen_height):
        pygame.draw.polygon(self.effect_surf, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                            [(0, 0), (random.randint(400, screen_width), 0),
                             (random.randint(0, screen_width), random.randint(screen_height // 2, screen_height))])

        pygame.draw.polygon(self.effect_surf, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                            [(0, screen_height), (random.randint(400, screen_width), screen_height),
                             (random.randint(0, screen_width), random.randint(0, screen_height // 2))])

        pygame.draw.polygon(self.effect_surf, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                            [(0, 0), (0, random.randint(400, screen_height)),
                             (random.randint(screen_width // 2, screen_width), random.randint(0, screen_height))])

        pygame.draw.polygon(self.effect_surf, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                            [(screen_width, 0), (screen_width, random.randint(400, screen_height)),
                             (random.randint(0, screen_width // 2), random.randint(0, screen_height))])



