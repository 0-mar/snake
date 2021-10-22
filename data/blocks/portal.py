import pygame
import random
import data.states.game_state


class Portal(pygame.sprite.Sprite):
    def __init__(self, game_world):
        pygame.sprite.Sprite.__init__(self)

        self.game_world = game_world
        self.game = self.game_world.game
        self.snake = self.game_world.snake

        self.map_width = data.states.game_state.MAP_WIDTH
        self.map_height = data.states.game_state.MAP_HEIGHT

        # load images
        self.portal_img = pygame.image.load("data/assets/portal.png")
        x, y = self.generate_pos()

        self.rect = pygame.rect.Rect(x, y, self.game.tile_size, self.game.tile_size)

    def update(self, *args, **kwargs) -> None:
        # check collision with the snake head
        if self.rect.colliderect(self.snake.segments[0].rect):
            self.game_world.gamemode.set_level(self.game_world.gamemode.level_number + 1)

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.portal_img, (self.rect.x - offset_x, self.rect.y - offset_y))

    def generate_pos(self):
        found_new_pos = False
        repeat = False
        new_x = 0
        new_y = 0

        while not found_new_pos:
            new_x = random.randint(0, (self.map_width // self.game.tile_size) - 1) * self.game.tile_size
            new_y = random.randint(0, (self.map_height // self.game.tile_size) - 1) * self.game.tile_size
            is_in_barrier = (new_x, new_y) in self.game_world.barriers.barrier_dict

            for segment in self.snake.segments:
                if segment.rect.x == new_x and segment.rect.y == new_y:
                    repeat = True
                    break

            if is_in_barrier:
                repeat = True

            if not repeat:
                found_new_pos = True
            else:
                repeat = False

        return (new_x, new_y)


