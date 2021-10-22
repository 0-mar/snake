import data.food.food
import random
import data.snake


class Hamburger(data.food.food.Food):
    def __init__(self, game, game_world, img_list, move_speed, axis, eat_sound):
        super().__init__(game, game_world, img_list, eat_sound)

        self.move_speed = move_speed
        self.ms = move_speed
        self.axis = axis
        self.collided = False

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.animation.image_mask_surface, (self.rect.x - 1 - offset_x, self.rect.y - 1 - offset_y))
        surface.blit(self.animation.image_mask_surface, (self.rect.x + 1 - offset_x, self.rect.y + 1 - offset_y))
        surface.blit(self.animation.image_mask_surface, (self.rect.x + 1 - offset_x, self.rect.y - 1 - offset_y))
        surface.blit(self.animation.image_mask_surface, (self.rect.x - 1 - offset_x, self.rect.y + 1 - offset_y))

        surface.blit(self.animation.current_image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

        # move the burger (and check collisions)
        if self.axis == 0:
            for block in self.get_barriers_around_block(self.rect.x + self.move_speed, self.rect.y):
                if block.colliderect(self.rect.x + self.move_speed, self.rect.y, self.game.tile_size,
                                     self.game.tile_size):
                    #print("KOLIZE")
                    if self.move_speed > 0:
                        self.rect.right = block.left
                    else:
                        self.rect.left = block.right

                    self.move_speed = -self.move_speed
                    self.collided = True
                    break
            if not self.collided:
                self.rect.x += self.move_speed
            else:
                self.collided = False

        else:
            for block in self.get_barriers_around_block(self.rect.x, self.rect.y + self.move_speed):
                if block.colliderect(self.rect.x, self.rect.y + self.move_speed, self.game.tile_size,
                                     self.game.tile_size):

                    if self.move_speed > 0:
                        self.rect.bottom = block.top
                    else:
                        self.rect.top = block.bottom

                    self.move_speed = -self.move_speed
                    self.collided = True
                    break

            if not self.collided:
                self.rect.y += self.move_speed
            else:
                self.collided = False

            # check if the burger is out of the screen and adjust its pos
        if self.rect.left >= self.map_width:
            self.rect.left = 0
        elif self.rect.right <= 0:
            self.rect.right = self.map_width

        if self.rect.bottom <= 0:
            self.rect.bottom = self.map_height
        elif self.rect.top >= self.map_height:
            self.rect.top = 0

    def on_snake_collide(self):
        self.active = False
        self.game_world.score += (3 * self.multiplier)
        new_x, new_y = self.snake.get_new_segment_pos()
        self.snake.segments.append(data.snake.SnakeSegment(new_x, new_y, 0, self.snake))
        new_x, new_y = self.snake.get_new_segment_pos()
        self.snake.segments.append(data.snake.SnakeSegment(new_x, new_y, 0, self.snake))
        new_x, new_y = self.snake.get_new_segment_pos()
        self.snake.segments.append(data.snake.SnakeSegment(new_x, new_y, 6, self.snake))

        self.snake.update_segment_images()

    def get_barriers_around_block(self, pos_x, pos_y):
        barriers = []
        offsets = [(0, 0), (0, -self.game.tile_size), (self.game.tile_size, -self.game.tile_size),
                   (self.game.tile_size, 0), (self.game.tile_size, self.game.tile_size),
                   (0, self.game.tile_size), (-self.game.tile_size, self.game.tile_size), (-self.game.tile_size, 0),
                   (-self.game.tile_size, -self.game.tile_size)]

        pos_x = (pos_x // self.game.tile_size) * self.game.tile_size
        pos_y = (pos_y // self.game.tile_size) * self.game.tile_size

        for offset in offsets:
            block = self.game_world.barriers.barrier_dict.get((pos_x + offset[0], pos_y + offset[1]))
            if block is not None:
                barriers.append(block)
                continue

            block = self.snake.get_segment_by_pos(pos_x + offset[0], pos_y + offset[1])
            if block is not None:
                barriers.append(block.rect)

        return barriers

    def reset(self):
        self.rect.x, self.rect.y = self.generate_new_pos()
        self.move_speed = random.randint(5, 16)
        self.axis = random.randint(0, 1)