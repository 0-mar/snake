import data.food.food
import random
import data.snake


class Banana(data.food.food.Food):
    def __init__(self, game, game_world, img_list, eat_sound):
        super().__init__(game, game_world, img_list, eat_sound)

        self.active = True

        self.counter = 0
        self.y_offset = 0
        self.move_by = 1

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.animation.image_mask_surface,
                     (self.rect.x - 1 - offset_x, self.rect.y - 1 + self.y_offset - offset_y))
        surface.blit(self.animation.image_mask_surface,
                     (self.rect.x + 1 - offset_x, self.rect.y + 1 + self.y_offset - offset_y))
        surface.blit(self.animation.image_mask_surface,
                     (self.rect.x + 1 - offset_x, self.rect.y - 1 + self.y_offset - offset_y))
        surface.blit(self.animation.image_mask_surface,
                     (self.rect.x - 1 - offset_x, self.rect.y + 1 + self.y_offset - offset_y))

        surface.blit(self.animation.current_image, (self.rect.x - offset_x, self.rect.y + self.y_offset - offset_y))

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

        self.counter += 1
        if self.counter >= 3:
            self.counter = 0
            self.y_offset += self.move_by
            if abs(self.y_offset) >= 2:
                self.move_by = -self.move_by

    def on_snake_collide(self):
        self.game_world.score += (1 * self.multiplier)
        new_x, new_y = self.snake.get_new_segment_pos()
        self.snake.segments.append(data.snake.SnakeSegment(new_x, new_y, 6, self.snake))

        self.snake.update_segment_images()

        self.rect.x, self.rect.y = self.generate_new_pos()

        val = random.randint(1, 4)

        if val == 1:
            self.game_world.food_list[1].active = True
            self.game_world.food_list[1].reset()

        elif val == 3:
            self.game_world.food_list[2].reset()
            self.game_world.food_list[2].active = True


class TemporaryBanana(Banana):
    def __init__(self, game, game_world, img_list, eat_sound):
        super(TemporaryBanana, self).__init__(game, game_world, img_list, eat_sound)

    def on_snake_collide(self):
        self.game_world.score += (1 * self.multiplier)
        new_x, new_y = self.snake.get_new_segment_pos()
        self.snake.segments.append(data.snake.SnakeSegment(new_x, new_y, 6, self.snake))

        self.snake.update_segment_images()
        self.active = False
