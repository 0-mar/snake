import pygame
import data.states.state as state
import data.buttons.button as button
import data.states.game_state as game_state


class GameOverState(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)

        # load images
        self.original_background_img = pygame.image.load("data/assets/background/game_over_background.png").convert_alpha()
        self.revive_btn_img = pygame.image.load("data/assets/button/revive_button.png").convert_alpha()
        self.exit_btn_img = pygame.image.load("data/assets/button/exit_button.png").convert_alpha()

        # colors
        self.violet = (77, 4, 145)
        self.black = (5, 5, 5)

        # fonts
        self.font = pygame.font.SysFont("bodonicondensed", 60)

        self.revive_btn = button.Button(0, 0, self.revive_btn_img)
        self.exit_btn = button.Button(0, 0, self.exit_btn_img)

        self.original_background_width = self.original_background_img.get_width()
        self.original_background_height = self.original_background_img.get_height()

        self.background_img = self.original_background_img
        self.background_rect = self.background_img.get_rect()

        self.resize(self.game.screen_width, self.game.screen_height)

    def draw_death_msg(self, surface, font, text_col):
        img = font.render("Chcipnul jsi sracko!", True, self.black)
        img_rect = img.get_rect()
        img_rect.center = (self.background_rect.centerx, self.background_rect.top + 50)

        surface.blit(img, (img_rect.x + 3, img_rect.y + 3))
        img = font.render("Chcipnul jsi sracko!", True, text_col)
        surface.blit(img, (img_rect.x, img_rect.y))

    def render(self, surface):
        self.prev_state.render(surface)
        surface.blit(self.background_img, self.background_rect)

        self.revive_btn.draw(surface)
        self.exit_btn.draw(surface)

        self.draw_death_msg(surface, self.font, self.violet)

    def update(self, time_passed):
        if self.exit_btn.update():
            self.game.state_stack[-1].exit_state()
            self.game.state_stack[-1].exit_state()
            self.game.state_stack[-1].exit_state()

        if self.revive_btn.update():
            self.game.state_stack[-1].exit_state()
            prev_gamemode = self.game.state_stack[-1].gamemode_number
            self.game.state_stack[-1].exit_state()

            game_world = game_state.GameState(self.game, prev_gamemode)
            game_world.enter_state()

    def resize(self, screen_width, screen_height):
        super(GameOverState, self).resize(screen_width, screen_height)

        self.background_img = pygame.transform.scale(self.original_background_img, (int(screen_width * (15/16)), int(screen_height * (125/256))))
        self.background_rect = self.background_img.get_rect()
        self.background_rect.left = int(screen_width * (1/32))
        self.background_rect.bottom = screen_height - int(screen_height * (1 / 16))

        self.revive_btn.scale_and_reposition(((self.background_rect.centerx - self.background_rect.left) // 2) + self.background_rect.left, self.background_rect.centery, self.scale)
        self.exit_btn.scale_and_reposition(((self.background_rect.right - self.background_rect.centerx) // 2) + self.background_rect.centerx, self.background_rect.centery, self.scale)

        self.ui_width = self.exit_btn.rect.right - self.revive_btn.rect.left + 50
        self.ui_height = self.exit_btn.rect.bottom - self.background_rect.top + 60