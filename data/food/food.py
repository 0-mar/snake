import pygame
import data.snake
import data.animation
import random

import data.states.game_state


class Food(pygame.sprite.Sprite):
    def __init__(self, game, game_world, img_list, eat_sound):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.game_world = game_world
        self.snake = game_world.snake

        self.eat_sound = eat_sound

        self.map_width = data.states.game_state.MAP_WIDTH
        self.map_height = data.states.game_state.MAP_HEIGHT

        x, y = self.generate_new_pos()
        self.rect = pygame.rect.Rect(x, y, self.game.tile_size, self.game.tile_size)

        self.animation = data.animation.Animation(img_list, 5, self.game)

        # multiplies the amount of score you get by eating this food
        self.multiplier = 1

        self.active = False

    def draw(self, surface, offset_x, offset_y):
        """if self.rect.x % self.game.tile_size != 0 or self.rect.y % self.game.tile_size != 0:
            raise ValueError(f"Jidlo nema validni souradnice ({self.rect.x} {self.rect.y}) - nedelitelne {self.game.tile_size}")"""
        pass

    def update(self, *args, **kwargs) -> None:
        self.animation.update()

        # check collision with the snake head (eating)
        if self.rect.colliderect(self.snake.segments[0].rect):
            self.eat_sound.play()
            self.on_snake_collide()

    def on_snake_collide(self):
        """This method gets called upon the collision of snake head with this instance. Override this method if you
        want anything to happen after the collision"""
        pass

    # generate new pos which is not inside of a barrier block, snake segment or food
    def generate_new_pos(self):
        found_new_pos = False
        new_x = 0
        new_y = 0
        repeat = False

        while not found_new_pos:
            new_x = random.randint(0, (self.map_width // self.game.tile_size) - 1) * self.game.tile_size
            new_y = random.randint(0, (self.map_height // self.game.tile_size) - 1) * self.game.tile_size
            is_in_barrier = (new_x, new_y) in self.game_world.barriers.barrier_dict

            for segment in self.snake.segments:
                if segment.rect.x == new_x and segment.rect.y == new_y:
                    repeat = True
                    break

            if repeat:
                repeat = False
                continue

            for f in self.game_world.food_list:
                if f.rect.x == new_x and f.rect.y == new_y:
                    repeat = True
                    break

            if repeat:
                repeat = False
                continue

            if is_in_barrier:
                repeat = True

            if not repeat:
                found_new_pos = True

        return (new_x, new_y)