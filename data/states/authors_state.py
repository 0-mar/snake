import data.states.state as state
import data.buttons.button as button
import pygame


class AuthorsState(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)

        # load images
        back_btn_img = pygame.image.load("data/assets/button/back_btn.png").convert_alpha()
        self.background_img = pygame.image.load("data/assets/background/main_menu_background.png").convert()
        self.original_ondra_img = pygame.image.load("data/assets/background/me.png")
        self.original_michal_img = pygame.image.load("data/assets/background/gej.png")

        # load sounds
        self.ondra_sound = pygame.mixer.Sound("data/assets/sounds/ondra.mp3")

        self.ondra_img = self.original_ondra_img
        self.michal_img = self.original_michal_img

        self.ondra_rect = self.ondra_img.get_rect()
        self.michal_rect = self.michal_img.get_rect()

        self.back_btn = button.Button(0, 0, back_btn_img)

        self.resize(self.game.screen_width, self.game.screen_height)

        self.ondra_sound.play(fade_ms=1000)

    def update(self, time_passed):
        if self.back_btn.update():
            self.game.state_stack[-1].exit_state()

    def render(self, surface):
        surface.blit(self.background_img, (0, 0))
        self.back_btn.draw(surface)

        surface.blit(self.ondra_img, self.ondra_rect)
        surface.blit(self.michal_img, self.michal_rect)

    def resize(self, screen_width, screen_height):
        super(AuthorsState, self).resize(screen_width, screen_height)
        
        self.ondra_img = pygame.transform.scale(self.original_ondra_img, (int(screen_width * (3/4)), int(screen_height * (1/3))))
        self.ondra_rect = self.ondra_img.get_rect()
        self.ondra_rect.topleft = (int(screen_width * (1 / 32)), int(screen_height * (1 / 32)))

        self.michal_img = pygame.transform.scale(self.original_michal_img,
                                                (int(screen_width * (3 / 4)), int(screen_height * (1 / 3))))
        self.michal_rect = self.michal_img.get_rect()
        self.michal_rect.bottomright = (screen_width - int(screen_width * (1 / 32)), screen_height - int(screen_height * (1 / 32)))

        self.back_btn.scale_and_reposition(screen_width // 2, screen_height // 2, self.scale)

        self.ui_width = self.back_btn.rect.right
        self.ui_height = self.back_btn.rect.bottom

    def exit_state(self):
        self.ondra_sound.stop()
        super(AuthorsState, self).exit_state()


