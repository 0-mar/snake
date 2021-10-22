import pygame


class Button:
    def __init__(self, x, y, image):
        self.original_width = image.get_width()
        self.original_height = image.get_height()
        self.original_image = image
        self.image = self.original_image

        self.hovered_over = False
        self.hovered_image = self.image.copy()
        self.hovered_image.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

        # load sounds
        self.click_sound = pygame.mixer.Sound("data/assets/sounds/click_sound.wav")

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.hovered_over:
            surface.blit(self.hovered_image, (self.rect.x, self.rect.y))

    def update(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.hovered_over = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.click_sound.play()
                action = True
                self.clicked = True
        else:
            self.hovered_over = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

    def scale_and_reposition(self, x, y, scale):
        self.image = pygame.transform.scale(self.original_image, (int(self.original_width * scale), int(self.original_height * scale)))
        self.hovered_image = self.image.copy()
        self.hovered_image.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class HighlightedButton(Button):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.highlighting_rect = pygame.rect.Rect(0, 0, 0, 0)

        self.gray = (173, 173, 173)
        self.green = (190, 196, 10)

    def draw(self, surface):
        if self.hovered_over:
            pygame.draw.rect(surface, self.gray, self.highlighting_rect)
        if self.clicked:
            pygame.draw.rect(surface, self.green, self.highlighting_rect)
        super().draw(surface)

    """def update(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.hovered_over = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        else:
            self.hovered_over = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action"""

    def scale_and_reposition(self, x, y, scale, screen_width):
        super().scale_and_reposition(x, y, scale)

        self.highlighting_rect.width = screen_width + 600
        self.highlighting_rect.height = self.rect.height + 40

        self.highlighting_rect.center = (x, y)
