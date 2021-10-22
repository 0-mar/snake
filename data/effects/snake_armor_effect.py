import data.effects.effect as effect


class SnakeArmorEffect(effect.Effect):
    def __init__(self, duration, game_state):
        super(SnakeArmorEffect, self).__init__(duration, game_state)

        self.snake = self.game_state.snake
        self.snake.armor = True

        self.snake.current_head_img = self.snake.armored_head_img
        self.snake.current_segment_img = self.snake.armored_segment_img
        self.snake.current_corner_bottom_right_img = self.snake.armored_corner_bottom_right_img
        self.snake.current_corner_left_top_img = self.snake.armored_corner_left_top_img
        self.snake.current_tail_img = self.snake.armored_tail_img

    def on_effect_disable(self):
        self.snake.armor = False

        self.snake.current_head_img = self.snake.snake_head_img
        self.snake.current_segment_img = self.snake.snake_segment_img
        self.snake.current_corner_bottom_right_img = self.snake.snake_corner_bottom_right_img
        self.snake.current_corner_left_top_img = self.snake.snake_corner_left_top_img
        self.snake.current_tail_img = self.snake.snake_tail_img

    def draw(self, surface):
        self.game_state.draw_text(surface, "Buldozér", self.effect_font, self.white, self.game_state.game.screen_width - 200, 20)
