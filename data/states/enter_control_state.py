import pygame
import data.states.state as state


class EnterControlState(state.State):
    def __init__(self, game, controls_manager, control_key, controls_state):
        super().__init__(game)
        self.controls_manager = controls_manager
        self.control_key = control_key
        self.controls_state = controls_state

        # load images
        self.original_background_img = pygame.image.load("data/assets/background/game_over_background.png").convert_alpha()

        # fonts
        self.font = pygame.font.SysFont("bodonicondensed", 60)

        # colors
        self.white = (240, 245, 250)

        self.background_img = self.original_background_img
        self.background_rect = self.background_img.get_rect()

        self.original_label_img = self.font.render("Zmackni klavesu", True, self.white)
        self.label_img = self.original_label_img
        self.label_rect = self.label_img.get_rect()

        self.resize(self.game.screen_width, self.game.screen_height)

    def render(self, surface):
        self.prev_state.render(surface)

        surface.blit(self.background_img, self.background_rect)
        surface.blit(self.label_img, self.label_rect)

    def update(self, time_passed):
        if self.game.last_key_pressed is not None:
            self.controls_manager.controls[self.control_key] = self.game.last_key_pressed
            self.controls_manager.write_controls(self.controls_manager.controls)
            """for k, v in self.controls_manager.controls.items():
                print(f"({k}: {pygame.key.name(v)})")"""

            self.controls_state.create_labels()
            self.exit_state()

    def resize(self, screen_width, screen_height):
        super().resize(screen_width, screen_height)

        self.background_img = pygame.transform.scale(self.original_background_img,
                                                     (int(screen_width * (15 / 16)), int(screen_height * (125 / 256))))
        self.background_rect = self.background_img.get_rect()
        self.background_rect.left = int(screen_width * (1 / 32))
        self.background_rect.bottom = screen_height - int(screen_height * (1 / 16))

        self.label_img = pygame.transform.scale(self.original_label_img, (int(self.original_label_img.get_width() * self.scale), int(self.original_label_img.get_height() * self.scale)))
        self.label_rect = self.label_img.get_rect()

        self.label_rect.center = self.background_rect.center

        self.ui_width = self.label_rect.right
        self.ui_height = self.label_rect.bottom