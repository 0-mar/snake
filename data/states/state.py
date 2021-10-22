class State:
    def __init__(self, g):
        self.game = g
        self.prev_state = None

        # scale of all elements in the GUI
        self.scale = 1
        self.scale_diff = 0.25

        self.ui_width = 0
        self.ui_height = 0

    def update(self, time_passed):
        pass

    def render(self, surface):
        pass

    def resize(self, screen_width, screen_height):
        """This method should be called whenever the window gets resized. Adjust positions of all GUI elements here.

        :param screen_width: new width of the window
        :param screen_height: new height of the window
        :param scale: scale of all elements in the GUI
        """
        self.adjust_scale(screen_width, screen_height)

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

        #self.resize(self.game.screen_width, self.game.screen_height, self.game.scale)
        self.game.on_resize_window(self.game.screen_width, self.game.screen_height)

    def exit_state(self):
        self.game.state_stack.pop()

        #self.resize(self.game.screen_width, self.game.screen_height, self.game.scale)
        self.game.on_resize_window(self.game.screen_width, self.game.screen_height)

    def adjust_scale(self, screen_width, screen_height):
        possible_scale = self.scale

        if self.ui_width > screen_width or self.ui_height > screen_height:
            while possible_scale > 1: #and (self.ui_width / self.scale) * (possible_scale) > screen_width or (self.ui_height / self.scale) * (possible_scale) > screen_height:
                if (self.ui_width / self.scale) * (possible_scale) > screen_width or (self.ui_height / self.scale) * (possible_scale) > screen_height:
                    possible_scale -= self.scale_diff
                else:
                    break

        elif (self.ui_width / self.scale) * (self.scale + self.scale_diff) <= screen_width and (self.ui_height / self.scale) * (self.scale + self.scale_diff) <= screen_height:
            while possible_scale < 2: #and (self.ui_width / self.scale) * (possible_scale) <= screen_width and (self.ui_height / self.scale) * (possible_scale) <= screen_height:
                if (self.ui_width / self.scale) * (possible_scale + self.scale_diff) <= screen_width and (self.ui_height / self.scale) * (possible_scale + self.scale_diff) <= screen_height:
                    possible_scale += self.scale_diff
                else:
                    break

        self.scale = possible_scale



