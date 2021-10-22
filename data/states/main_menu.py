import pygame
import data.states.state as state
import data.buttons.button as button
import data.states.authors_state as authors_state
import data.states.controls_state as controls_state
import data.states.gamemode_state as gamemode_state


class MainMenu(state.State):
    def __init__(self, g):
        state.State.__init__(self, g)

        # load images
        self.main_menu_background_img = pygame.image.load("data/assets/background/main_menu_background.png").convert()
        self.original_logo_img = pygame.image.load("data/assets/background/snake_logo.png").convert_alpha()
        self.play_btn_img = pygame.image.load("data/assets/button/play_btn.png").convert_alpha()
        self.exit_btn_img = pygame.image.load("data/assets/button/end_btn.png").convert_alpha()
        self.authors_btn_img = pygame.image.load("data/assets/button/authors_btn.png").convert_alpha()
        self.controls_btn_img = pygame.image.load("data/assets/button/controls_btn.png").convert_alpha()

        self.play_btn = button.Button(0, 0, self.play_btn_img)
        self.exit_btn = button.Button(0, 0, self.exit_btn_img)
        self.authors_btn = button.Button(0, 0, self.authors_btn_img)
        self.controls_btn = button.Button(0, 0, self.controls_btn_img)

        self.original_logo_width = self.original_logo_img.get_width()
        self.original_logo_height = self.original_logo_img.get_height()

        self.logo_img = self.original_logo_img
        self.logo_rect = self.logo_img.get_rect()

        self.resize(self.game.screen_width, self.game.screen_height)

    def update(self, time_passed):
        if self.exit_btn.update():
            self.game.running = False

        if self.play_btn.update():
            """game_world = game_state.GameState(self.game)
            game_world.enter_state()"""

            gamemode = gamemode_state.GamemodeState(self.game)
            gamemode.enter_state()

        if self.authors_btn.update():
            authors = authors_state.AuthorsState(self.game)
            authors.enter_state()

        if self.controls_btn.update():
            controls = controls_state.ControlsState(self.game)
            controls.enter_state()

    def render(self, surface):
        surface.blit(self.main_menu_background_img, (0, 0))
        surface.blit(self.logo_img, self.logo_rect)

        self.play_btn.draw(surface)
        self.exit_btn.draw(surface)
        self.authors_btn.draw(surface)
        self.controls_btn.draw(surface)

    def resize(self, screen_width, screen_height):
        super().resize(screen_width, screen_height)
        
        centre = screen_width // 2
        vertical_gap = 50 * self.scale

        self.logo_img = pygame.transform.scale(self.original_logo_img, (int(self.original_logo_width * self.scale), int(self.original_logo_height * self.scale)))
        self.logo_rect = self.logo_img.get_rect()
        self.logo_rect.center = (centre, self.logo_rect.center[1])
        self.logo_rect.top = vertical_gap / 2

        #self.play_btn.scale_and_reposition(centre, (2 * vertical_gap) + self.logo_img.get_height(), self.scale)
        #self.exit_btn.scale_and_reposition(centre, (3 * vertical_gap) + self.logo_img.get_height() + self.play_btn.image.get_height(), self.scale)
        self.play_btn.scale_and_reposition(centre, vertical_gap + self.logo_rect.bottom, self.scale)
        self.controls_btn.scale_and_reposition(centre, vertical_gap + self.play_btn.rect.bottom, self.scale)
        self.authors_btn.scale_and_reposition(centre, vertical_gap + self.controls_btn.rect.bottom, self.scale)
        self.exit_btn.scale_and_reposition(centre, vertical_gap + self.authors_btn.rect.bottom, self.scale)

        #self.ui_height = (3 * vertical_gap) + self.logo_img.get_height() + self.play_btn.image.get_height() + self.exit_btn.image.get_height()
        self.ui_height = self.exit_btn.rect.bottom
        self.ui_width = self.logo_rect.width


