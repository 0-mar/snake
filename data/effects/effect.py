import pygame


class Effect:
    def __init__(self, duration, game_state):
        # font
        self.effect_font = pygame.font.SysFont("microsoftsansserif", 40)

        # colors
        self.white = pygame.Color(255, 255, 255)

        self.duration = duration
        self.game_state = game_state

        self.cam = self.game_state.cam

        self.duration_counter = 0
        self.active = True

        self.extend_existing_effect_duration()

    def update(self):
        #print(f"uplynulo {self.duration_counter} z {self.duration}")

        self.duration_counter += 1
        if self.duration_counter >= self.duration:
            self.active = False
            self.on_effect_disable()

    def draw(self, surface):
        pass

    def on_effect_disable(self):
        #self.game_state.effects_list.remove(self)
        pass

    def extend_existing_effect_duration(self):
        for effect in self.game_state.effects_list:
            if type(effect) == self.__class__:
                effect.duration_counter += self.duration_counter
                self.active = False



