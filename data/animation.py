import pygame


class Animation:

    def __init__(self, image_sequence, timer, game):
        self.game = game
        self.image_sequence = image_sequence
        self.index = 0

        self.current_image = image_sequence[self.index]
        self.image_mask_surface = self.update_image_mask()

        self.timer = timer
        self.game = game
        self.counter = 0

    def update(self):
        self.counter += 1

        if self.counter >= self.timer:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.image_sequence):
                self.index = 0

            self.current_image = self.image_sequence[self.index]
            self.image_mask_surface = self.update_image_mask()

        return self.current_image

    def update_image_mask(self):
        image_mask = pygame.mask.from_surface(self.current_image)
        image_mask.invert()
        image_mask_surface = image_mask.to_surface()
        image_mask_surface.set_colorkey(self.game.white)

        return image_mask_surface
