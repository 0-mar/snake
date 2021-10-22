import data.food.banana
import data.effects.invert_controls_effect as invert_controls_effect
import data.effects.double_score_effect as double_score_effect
import data.effects.shrink_snake_effect as shrink_snake_effect
import data.effects.random_barriers_effect as random_barriers_effect
import data.effects.banana_cluster_effect as banana_cluster_effect
import data.effects.snake_armor_effect as snake_armor_effect

import random


class Mushroom(data.food.banana.Banana):
    def __init__(self, game, game_world, img_list, eat_sound):
        super().__init__(game, game_world, img_list, eat_sound)

        self.active = False
        self.duration = random.randint(self.game.fps * 5, self.game.fps * 10)
        self.duration_counter = 0

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

        self.duration_counter += 1
        if self.duration_counter >= self.duration:
            self.active = False

    def on_snake_collide(self):
        self.active = False
        effect_duration = random.randint(self.game.fps * 5, self.game.fps * 10)

        val = random.randint(0, 5)
        if val == 0:
            self.game_world.effects_list.append(invert_controls_effect.InvertControlsEffect(effect_duration, self.game_world))
        elif val == 1:
            self.game_world.effects_list.append(double_score_effect.DoubleScoreEffect(effect_duration, self.game_world))
        elif val == 2:
            self.game_world.effects_list.append(shrink_snake_effect.ShrinkSnakeEffect(effect_duration, self.game_world, self.rect.x, self.rect.y))
        elif val == 3:
            self.game_world.effects_list.append(random_barriers_effect.RandomBarriersEffect(effect_duration, self.game_world))
        elif val == 4:
            self.game_world.effects_list.append(banana_cluster_effect.BananaClusterEffect(effect_duration, self.game_world))
        elif val == 5:
            self.game_world.effects_list.append(snake_armor_effect.SnakeArmorEffect(effect_duration, self.game_world))

    def reset(self):
        self.rect.x, self.rect.y = self.generate_new_pos()
        self.duration_counter = 0
        self.duration = random.randint(self.game.fps * 5, self.game.fps * 10)