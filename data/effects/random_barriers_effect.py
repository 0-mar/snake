import data.effects.effect as effect
import data.states.game_state
import pygame
import data.barrier
import random

obstacles = [[[1, 0, 0, 0, 0, 0, 1, 1],
             [1, 0, 0, 0, 0, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1]],

             [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 0, 0, 1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1]],

             [[1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 0, 0]],

             [[1, 1],
              [1, 1],
              [1, 1],
              [1, 1],
              [1, 1],
              [1, 1],
              [1, 1],
              [1, 1],
              [1, 1]],

             [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]]


class RandomBarriersEffect(effect.Effect):
    def __init__(self, duration, game_state):
        super(RandomBarriersEffect, self).__init__(duration, game_state)

        self.game = self.game_state.game
        self.map_width = data.states.game_state.MAP_WIDTH
        self.map_height = data.states.game_state.MAP_HEIGHT

        self.obstacle = random.choice(obstacles)
        self.obstacle_rect = self.create_hitbox()

        self.barrier_dict_keys = self.game_state.barriers.create_temporary_barrier_chunk(self.obstacle_rect.x,
                                                                                         self.obstacle_rect.y,
                                                                                         self.obstacle)

    def on_effect_disable(self):
        for pair in self.barrier_dict_keys:
            del self.game_state.barriers.barrier_dict[pair]

    def create_hitbox(self):
        width = len(self.obstacle[0]) * self.game.tile_size
        height = len(self.obstacle) * self.game.tile_size

        obstacle_rect = pygame.rect.Rect(0, 0, width, height)

        obstacle_rect.topleft = self.generate_pos(obstacle_rect.width, obstacle_rect.height)

        return obstacle_rect

    def generate_pos(self, width, height):
        found_new_pos = False
        colliding = False
        new_x = 0
        new_y = 0

        obstacle_rect = pygame.rect.Rect(0, 0, width, height)

        while not found_new_pos:
            new_x = random.randint(0, (self.map_width // self.game.tile_size) - 1) * self.game.tile_size
            new_y = random.randint(0, (self.map_height // self.game.tile_size) - 1) * self.game.tile_size
            obstacle_rect.topleft = (new_x, new_y)

            for segment in self.game_state.snake.segments:
                if obstacle_rect.colliderect(segment.rect):
                    colliding = True
                    break

            if not colliding:
                found_new_pos = True
            else:
                colliding = False

        return (new_x, new_y)

