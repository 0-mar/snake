import pygame
import data.states.state as state
import data.buttons.button as button
import data.controls
import data.states.enter_control_state as enter_control_state


class ControlsState(state.State):
    def __init__(self, game):
        super().__init__(game)
        self.controls_manager = data.controls.ControlsManager()
        self.controls = self.controls_manager.controls

        # load images
        self.background_img = pygame.image.load("data/assets/background/main_menu_background.png").convert()
        back_btn_img = pygame.image.load("data/assets/button/back_btn.png").convert_alpha()
        self.original_controls_title_img = pygame.image.load("data/assets/background/controls_title.png")

        # fonts
        #self.font = pygame.font.SysFont("Futura", 60)
        self.font = pygame.font.SysFont("bodonicondensed", 60)
        #self.font = pygame.font.SysFont("imprintshadow", 50)
        #self.font = pygame.font.SysFont("impact", 50)

        # colors
        self.violet = (77, 4, 145)
        self.lighter_violet = (120, 3, 173)

        self.controls_title_img = self.original_controls_title_img
        self.controls_title_rect = self.controls_title_img.get_rect()

        self.back_btn = button.Button(0, 0, back_btn_img)

        """self.up_btn = button.Button(0, 0, self.font.render("Nahoru", True, self.violet))
        self.down_btn = button.Button(0, 0, self.font.render("Dolu", True, self.violet))
        self.left_btn = button.Button(0, 0, self.font.render("Doleva", True, self.violet))
        self.right_btn = button.Button(0, 0, self.font.render("Doprava", True, self.violet))"""

        self.up_btn = button.HighlightedButton(0, 0, self.font.render("Nahoru", True, self.violet))
        self.down_btn = button.HighlightedButton(0, 0, self.font.render("Dolu", True, self.violet))
        self.left_btn = button.HighlightedButton(0, 0, self.font.render("Doleva", True, self.violet))
        self.right_btn = button.HighlightedButton(0, 0, self.font.render("Doprava", True, self.violet))

        self.control_btns = [self.up_btn, self.down_btn, self.left_btn, self.right_btn]

        self.original_label_imgs = []
        self.label_imgs = []
        self.label_rects = []

        self.create_labels()

        """self.original_up_option_img = self.font.render("Nahoru", True, self.violet)
        self.up_option_img = self.original_up_option_img
        self.up_option_rect = self.up_option_img.get_rect()"""

        self.resize(self.game.screen_width, self.game.screen_height)

    def update(self, time_passed):
        if self.back_btn.update():
            self.game.state_stack[-1].exit_state()

        if self.up_btn.update():
            self.game.last_key_pressed = None
            window = enter_control_state.EnterControlState(self.game, self.controls_manager, "up", self)
            window.enter_state()

        if self.down_btn.update():
            self.game.last_key_pressed = None
            window = enter_control_state.EnterControlState(self.game, self.controls_manager, "down", self)
            window.enter_state()

        if self.left_btn.update():
            self.game.last_key_pressed = None
            window = enter_control_state.EnterControlState(self.game, self.controls_manager, "left", self)
            window.enter_state()

        if self.right_btn.update():
            self.game.last_key_pressed = None
            window = enter_control_state.EnterControlState(self.game, self.controls_manager, "right", self)
            window.enter_state()

    def render(self, surface):
        surface.blit(self.background_img, (0, 0))
        surface.blit(self.controls_title_img, self.controls_title_rect)

        for btn in self.control_btns:
            btn.draw(surface)

        for i, label in enumerate(self.label_imgs):
            surface.blit(label, self.label_rects[i])

        self.back_btn.draw(surface)

    def resize(self, screen_width, screen_height):
        super().resize(screen_width, screen_height)

        self.controls_title_img = pygame.transform.scale(self.original_controls_title_img, (int(self.original_controls_title_img.get_width() * self.scale), int(self.original_controls_title_img.get_height() * self.scale)))
        self.controls_title_rect = self.controls_title_img.get_rect()
        self.controls_title_rect.centerx = screen_width // 2
        self.controls_title_rect.top = int(screen_height * (1/30))

        self.resize_control_buttons(screen_width, screen_height)
        self.resize_labels(screen_width, screen_height)

        self.back_btn.scale_and_reposition(screen_width // 2, screen_height - int(screen_height * (1/10)), self.scale)

        self.ui_width = self.controls_title_rect.right
        self.ui_height = self.back_btn.rect.bottom

    def resize_control_buttons(self, screen_width, screen_height):
        for i, btn in enumerate(self.control_btns):
            if i == 0:
                btn.scale_and_reposition(screen_width // 4, self.controls_title_rect.bottom + (screen_height // 10), self.scale, screen_width)
            else:
                btn.scale_and_reposition(screen_width // 4, self.control_btns[i - 1].rect.bottom + (screen_height // 10), self.scale, screen_width)

    def create_labels(self):
        self.original_label_imgs = []
        self.label_imgs = []
        self.label_rects = []

        for label in self.controls.values():
            #print(pygame.key.name(label))
            new_img = self.font.render(pygame.key.name(label), True, self.lighter_violet)
            self.original_label_imgs.append(new_img)
            self.label_imgs.append(new_img)
            self.label_rects.append(new_img.get_rect())

    def resize_labels(self, screen_width, screen_height):
        for i in range(len(self.original_label_imgs)):
            resized_img = pygame.transform.scale(self.original_label_imgs[i], (int(self.original_label_imgs[i].get_width() * self.scale), int(self.original_label_imgs[i].get_height() * self.scale)))
            resized_rect = resized_img.get_rect()

            resized_rect.right = screen_width - (screen_width // 10)
            resized_rect.top = self.control_btns[i].rect.top

            self.label_rects[i] = resized_rect
            self.label_imgs[i] = resized_img






