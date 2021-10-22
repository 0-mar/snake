import data.states.game_state


class Camera:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake
        self.offset_x = 0
        self.offset_y = 0

    def scroll_camera(self):
        self.offset_x += self.snake.segments[0].rect.x - self.offset_x - (self.game.screen_width / 2)
        self.offset_y += self.snake.segments[0].rect.y - self.offset_y - (self.game.screen_height / 2)

        self.offset_x = max(0, self.offset_x)
        self.offset_x = min(data.states.game_state.MAP_WIDTH - self.game.screen_width, self.offset_x)

        self.offset_y = max(0, self.offset_y)
        self.offset_y = min(data.states.game_state.MAP_HEIGHT - self.game.screen_height, self.offset_y)

        #print(f"offset X: {self.offset_x}, offset Y: {self.offset_y}")

        """if self.offset_x < 0:
            self.offset_x = 0
        elif self.offset_x > states.game_state.MAP_WIDTH - self.game.screen_width:
            self.offset_x = states.game_state.MAP_WIDTH - self.game.screen_width

        if self.offset_y < 0:
            self.offset_y = 0
        elif self.offset_y > states.game_state.MAP_HEIGHT - self.game.screen_height:
            self.offset_y = states.game_state.MAP_HEIGHT - self.game.screen_height"""
