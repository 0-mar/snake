import data.states.state as state
import data.buttons.button as button
import pygame
import data.states.game_state as game_state


class GamemodeState(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)

        # load images
        levels_btn_img = pygame.image.load("data/assets/button/levels_btn.png").convert_alpha()
        infinite_btn_img = pygame.image.load("data/assets/button/infinite_btn.png").convert_alpha()
        self.background_img = pygame.image.load("data/assets/background/main_menu_background.png").convert()
        self.original_gamemodes_title_img = pygame.image.load("data/assets/background/gamemodes_title.png")

        self.infinite_btn = button.Button(0, 0, infinite_btn_img)
        self.levels_btn = button.Button(0, 0, levels_btn_img)
        
        self.gamemodes_title_img = self.original_gamemodes_title_img
        self.gamemodes_title_rect = self.gamemodes_title_img.get_rect()

    def update(self, time_passed):
        if self.infinite_btn.update():
            game_world = game_state.GameState(self.game, 0)
            game_world.enter_state()
        elif self.levels_btn.update():
            game_world = game_state.GameState(self.game, 1)
            game_world.enter_state()

    def render(self, surface):
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.gamemodes_title_img, self.gamemodes_title_rect)
        self.infinite_btn.draw(surface)
        self.levels_btn.draw(surface)

    def resize(self, screen_width, screen_height):
        super(GamemodeState, self).resize(screen_width, screen_height)

        self.infinite_btn.scale_and_reposition(screen_width // 2, (screen_height // 2) - (screen_height // 10), self.scale)
        self.levels_btn.scale_and_reposition(screen_width // 2, (screen_height // 2) + (screen_height // 5), self.scale)

        self.gamemodes_title_img = pygame.transform.scale(self.original_gamemodes_title_img,
                                                          (int(self.original_gamemodes_title_img.get_width() * self.scale),
                                                           int(self.original_gamemodes_title_img.get_height() * self.scale)))
        self.gamemodes_title_rect = self.gamemodes_title_img.get_rect()
        self.gamemodes_title_rect.centerx = screen_width // 2
        self.gamemodes_title_rect.top = int(screen_height * (1 / 30))

        self.ui_width = self.gamemodes_title_rect.right

