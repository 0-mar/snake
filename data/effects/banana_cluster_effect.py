import data.effects.effect as effect
import random
import data.states.game_state
import data.food.banana as banana


class BananaClusterEffect(effect.Effect):
    def __init__(self, duration, game_state):
        super(BananaClusterEffect, self).__init__(duration, game_state)

        self.game = self.game_state.game
        self.map_width = data.states.game_state.MAP_WIDTH
        self.map_height = data.states.game_state.MAP_HEIGHT

        pos_x = random.randint(0, (self.map_width // self.game.tile_size) - 1) * self.game.tile_size
        pos_y = random.randint(0, (self.map_height // self.game.tile_size) - 1) * self.game.tile_size

        self.generate_bananas(pos_x, pos_y)

    def generate_bananas(self, pos_x, pos_y):
        for tile_y in range(0, 8):
            y = pos_y + (tile_y * self.game.tile_size)
            for tile_x in range(0, 8):
                x = pos_x + (tile_x * self.game.tile_size)

                if self.is_pos_valid(x, y):
                    banan = banana.TemporaryBanana(self.game, self.game_state, self.game_state.banan_list, self.game_state.eat_sound)
                    banan.rect.x = x
                    banan.rect.y = y

                    self.game_state.food_list.append(banan)

    def on_effect_disable(self):
        for f in self.game_state.food_list:
            if type(f) == banana.TemporaryBanana:
                f.active = False

    def is_pos_valid(self, x, y):
        """Determines whether there is something else on the given position

            :param x: x coordinate
            :param y: y coordinate"""

        is_in_barrier = (x, y) in self.game_state.barriers.barrier_dict
        if is_in_barrier:
            return False

        for segment in self.game_state.snake.segments:
            if segment.rect.x == x and segment.rect.y == y:
                return False

        for f in self.game_state.food_list:
            if f.rect.x == x and f.rect.y == y:
                return False

        return True
