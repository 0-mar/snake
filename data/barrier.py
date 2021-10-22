import pygame


class Barrier(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # load images
        self.barrier_img = pygame.image.load("data/assets/bricks.png").convert_alpha()

        # self.barrier_blocks = []
        self.barrier_dict = {}

    def create_barrier_chunk(self, x, y, barrier_data):
        tile_y = 0
        for row in barrier_data:
            tile_x = 0
            for tile in row:
                if tile == 1:
                    block = pygame.rect.Rect(x + (self.game.tile_size * tile_x), y + (self.game.tile_size * tile_y), self.game.tile_size,
                                             self.game.tile_size)
                    # self.barrier_blocks.append(block)
                    self.barrier_dict[(x + (self.game.tile_size * tile_x), y + (self.game.tile_size * tile_y))] = block
                tile_x += 1

            tile_y += 1

    def create_temporary_barrier_chunk(self, x, y, barrier_data):
        barrier_keys = []
        tile_y = 0
        for row in barrier_data:
            tile_x = 0
            for tile in row:
                if tile == 1:
                    pos_x = x + (self.game.tile_size * tile_x)
                    pos_y = y + (self.game.tile_size * tile_y)
                    if not (pos_x, pos_y) in self.barrier_dict:
                        block = pygame.rect.Rect(pos_x, pos_y, self.game.tile_size, self.game.tile_size)
                        # self.barrier_blocks.append(block)
                        self.barrier_dict[(pos_x, pos_y)] = block
                        barrier_keys.append((pos_x, pos_y))
                tile_x += 1

            tile_y += 1

        return barrier_keys

    def load_from_file(self, path):
        self.barrier_dict = {}

        with open(path) as file:
            for tile_y, row in enumerate(file.readlines()):
                for tile_x, char in enumerate(row):
                    if char == "1":
                        block = pygame.rect.Rect(self.game.tile_size * tile_x, self.game.tile_size * tile_y,
                                                 self.game.tile_size,
                                                 self.game.tile_size)
                        # self.barrier_blocks.append(block)
                        self.barrier_dict[
                            (self.game.tile_size * tile_x, self.game.tile_size * tile_y)] = block

    def update(self, *args, **kwargs) -> None:
        pass

    def draw(self, surface, offset_x, offset_y):
        for barrier in self.barrier_dict.values():
            if barrier.x % 16 != 0 or barrier.y % 16 != 0:
                raise ValueError(f"Barierovy blok nema validni souradnice ({barrier.x} {barrier.y}) - nedelitelne 16")
            surface.blit(self.barrier_img, (barrier.x - offset_x, barrier.y - offset_y))
