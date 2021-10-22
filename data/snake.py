import pygame
import data.states.game_state
import data.states.game_over_state
import data.controls


class Snake(pygame.sprite.Sprite):

    def __init__(self, x, y, game, game_world):
        pygame.sprite.Sprite.__init__(self)

        # load images
        self.snake_head_img = pygame.image.load("data/assets/snake/snake_head.png").convert_alpha()
        self.snake_segment_img = pygame.image.load("data/assets/snake/snake_tile.png").convert_alpha()
        self.snake_corner_bottom_right_img = pygame.image.load("data/assets/snake/snake_corner_outside.png").convert_alpha()
        self.snake_corner_left_top_img = pygame.image.load("data/assets/snake/snake_corner_inside.png").convert_alpha()
        self.snake_tail_img = pygame.image.load("data/assets/snake/snake_tail.png").convert_alpha()

        self.armored_head_img = pygame.image.load("data/assets/snake/armored_head.png").convert_alpha()
        self.armored_segment_img = pygame.image.load("data/assets/snake/armored_tile.png").convert_alpha()
        self.armored_corner_bottom_right_img = pygame.image.load("data/assets/snake/armored_corner_outside.png").convert_alpha()
        self.armored_corner_left_top_img = pygame.image.load("data/assets/snake/armored_corner_inside.png").convert_alpha()
        self.armored_tail_img = pygame.image.load("data/assets/snake/armored_tail.png").convert_alpha()

        # load sounds
        self.break_sound = pygame.mixer.Sound("data/assets/sounds/break_sound.mp3")
        self.crash_sound = pygame.mixer.Sound("data/assets/sounds/naraz_do_zdi.mp3")

        self.current_head_img = self.snake_head_img
        self.current_segment_img = self.snake_segment_img
        self.current_corner_bottom_right_img = self.snake_corner_bottom_right_img
        self.current_corner_left_top_img = self.snake_corner_left_top_img
        self.current_tail_img = self.snake_tail_img

        self.game = game
        self.game_world = game_world

        self.map_width = data.states.game_state.MAP_WIDTH
        self.map_height = data.states.game_state.MAP_HEIGHT

        self.segments = [SnakeSegment(x, y, 1, self), SnakeSegment(x - self.game.tile_size, y, 0, self),
                         SnakeSegment(x - self.game.tile_size * 2, y, 6, self)]

        # make the snake move 1 tile per Snake.update() call
        self.move_speed = self.game.tile_size * self.game.fps

        self.vel_x = 0
        self.vel_y = 0

        self.direction = "right"

        self.armor = False

        self.controls_manager = data.controls.ControlsManager()
        self.controls = self.controls_manager.controls

    def draw(self, surface, offset_x, offset_y):

        for s in self.segments:
            surface.blit(s.segment_mask_surface, (s.rect.x - 1 - offset_x, s.rect.y - 1 - offset_y))
            surface.blit(s.segment_mask_surface, (s.rect.x + 1 - offset_x, s.rect.y + 1 - offset_y))
            surface.blit(s.segment_mask_surface, (s.rect.x + 1 - offset_x, s.rect.y - 1 - offset_y))
            surface.blit(s.segment_mask_surface, (s.rect.x - 1 - offset_x, s.rect.y + 1 - offset_y))

        for idx, s in enumerate(self.segments):
            if s.rect.x % 16 != 0 or s.rect.y % 16 != 0:
                raise ValueError(f"Segment nema validni souradnice ({s.rect.x} {s.rect.y}) - nedelitelne 16")
            surface.blit(s.image, (s.rect.x - offset_x, s.rect.y - offset_y))

        """for s in self.segments:
            surface.blit(s.segment_mask_surface, (s.rect.x - 1, s.rect.y - 1))
            surface.blit(s.segment_mask_surface, (s.rect.x + 1, s.rect.y + 1))
            surface.blit(s.segment_mask_surface, (s.rect.x + 1, s.rect.y - 1))
            surface.blit(s.segment_mask_surface, (s.rect.x - 1, s.rect.y + 1))

        for s in self.segments:
            if s.rect.x % 16 != 0 or s.rect.y % 16 != 0:
                raise ValueError(f"Segment nema validni souradnice ({s.rect.x} {s.rect.y}) - nedelitelne 16")
            surface.blit(s.image, s.rect)"""

    def update(self, *args, **kwargs) -> None:
        # handle keypresses
        key = pygame.key.get_pressed()
        #if key[pygame.K_UP] and self.direction != "down":
        if key[self.controls["up"]] and self.direction != "down":
            self.vel_y = round(args[0] * -self.move_speed)
            self.vel_x = 0
            self.direction = "up"
        elif key[self.controls["down"]] and self.direction != "up":
            self.vel_y = round(args[0] * self.move_speed)
            self.vel_x = 0
            self.direction = "down"
        elif key[self.controls["left"]] and self.direction != "right":
            self.vel_x = round(args[0] * -self.move_speed)
            self.vel_y = 0
            self.direction = "left"
        elif key[self.controls["right"]] and self.direction != "left":
            self.vel_x = round(args[0] * self.move_speed)
            self.vel_y = 0
            self.direction = "right"
        elif key[pygame.K_SPACE]:
            self.vel_x = 0
            self.vel_y = 0
        elif key[pygame.K_q]:
            game_over = data.states.game_over_state.GameOverState(self.game)
            game_over.enter_state()
            print()
            print("UKONCENI QCKEM")

        # print(f"pos_x: {self.segments[0].rect.x} | pos_y: {self.segments[0].rect.y}")

        if self.vel_x != 0 and self.vel_x % self.game.tile_size != 0:
            self.vel_x = self.game.tile_size

        if self.vel_y != 0 and self.vel_y % self.game.tile_size != 0:
            self.vel_y = self.game.tile_size

        # move the snake
        if self.vel_x != 0 or self.vel_y != 0:  # checks if the snake is moving, otherwise this rendering is not correct!
            new_x = self.segments[0].rect.x + self.vel_x
            new_y = self.segments[0].rect.y + self.vel_y

            # if the snake went past the map border (0 or 1024), adjust its position
            if new_x + self.game.tile_size > data.states.game_state.MAP_WIDTH:
                new_x = 0
            elif new_x < 0:
                new_x = data.states.game_state.MAP_WIDTH - self.game.tile_size
            if new_y + self.game.tile_size > data.states.game_state.MAP_HEIGHT:
                new_y = 0
            elif new_y < 0:
                new_y = data.states.game_state.MAP_HEIGHT - self.game.tile_size

            # check for collision with barriers
            if (new_x, new_y) in self.game_world.barriers.barrier_dict:
                if self.armor:
                    self.break_sound.play()
                    del self.game_world.barriers.barrier_dict[(new_x, new_y)]
                else:
                    print()
                    print("NARAZ DO BARIERY")
                    self.crash_sound.play()
                    game_over = data.states.game_over_state.GameOverState(self.game)
                    game_over.enter_state()
                    return None

            # delete last segment and create a new one in order to create the illusion of movement
            new_head = SnakeSegment(new_x, new_y, 1, self)
            self.segments.insert(0, new_head)
            self.segments.pop()

        # check collision with tail
        for segment in self.segments[1:]:
            if self.segments[0].rect.colliderect(segment.rect):

                game_over = data.states.game_over_state.GameOverState(self.game)
                game_over.enter_state()
                print()
                print(f"NARAZ DO OCASU - pozice ocasu: ({segment.rect}) || pozice hlavy: ({self.segments[0].rect})")
                break

        # update segment images based on the shape of the snake
        self.update_segment_images()

    def update_segment_images(self):
        """Assigns proper image for each segment of the snake"""
        for i, segment in enumerate(self.segments):
            # rotate the head
            if i == 0:
                segment.set_image_number(1)
                if self.segments[1].rect.x > segment.rect.x:
                    # flips the snake head horizontally
                    segment.image = pygame.transform.flip(segment.image, True, False)
                elif self.segments[1].rect.y > segment.rect.y:
                    # rotates the snake head upwards
                    segment.image = pygame.transform.rotate(segment.image, 90)
                elif self.segments[1].rect.y < segment.rect.y:
                    # rotates the snake head downwards
                    segment.image = pygame.transform.rotate(segment.image, -90)

                if abs(segment.rect.x - self.segments[i + 1].rect.x) > self.game.tile_size:
                    segment.image = pygame.transform.flip(segment.image, True, False)
                elif abs(segment.rect.y - self.segments[i + 1].rect.y) > self.game.tile_size:
                    segment.image = pygame.transform.flip(segment.image, False, True)

            # adjust the tail
            elif i == len(self.segments) - 1:
                segment.set_image_number(6)
                if self.segments[i - 1].rect.y == segment.rect.y and self.segments[i - 1].rect.x > segment.rect.x:
                    pass
                elif self.segments[i - 1].rect.y == segment.rect.y and self.segments[i - 1].rect.x < segment.rect.x:
                    segment.image = pygame.transform.flip(segment.image, True, False)
                elif self.segments[i - 1].rect.x == segment.rect.x and self.segments[i - 1].rect.y > segment.rect.y:
                    segment.image = pygame.transform.rotate(segment.image, -90)
                else:
                    segment.image = pygame.transform.rotate(segment.image, 90)

                if abs(segment.rect.x - self.segments[i - 1].rect.x) > self.game.tile_size:
                    segment.image = pygame.transform.flip(segment.image, True, False)
                elif abs(segment.rect.y - self.segments[i - 1].rect.y) > self.game.tile_size:
                    segment.image = pygame.transform.flip(segment.image, False, True)

            else:
                if self.segments[i - 1].rect.y == segment.rect.y == self.segments[i + 1].rect.y:
                    segment.set_image_number(0)
                elif self.segments[i - 1].rect.x == segment.rect.x == self.segments[i + 1].rect.x:
                    segment.set_image_number(0)
                    segment.image = pygame.transform.rotate(segment.image, 90)

                # check for corner segments in the body
                elif self.segments[i - 1].rect.x >= segment.rect.x and self.segments[i - 1].rect.y >= segment.rect.y and \
                        self.segments[i + 1].rect.x >= segment.rect.x and self.segments[i + 1].rect.y >= segment.rect.y:
                    segment.set_image_number(2)
                elif self.segments[i - 1].rect.x <= segment.rect.x and self.segments[i - 1].rect.y >= segment.rect.y and \
                        self.segments[i + 1].rect.y >= segment.rect.y and self.segments[i + 1].rect.x <= segment.rect.x:
                    segment.set_image_number(3)
                elif self.segments[i - 1].rect.x <= segment.rect.x and self.segments[i - 1].rect.y <= segment.rect.y and \
                        self.segments[i + 1].rect.y <= segment.rect.y and self.segments[i + 1].rect.x <= segment.rect.x:
                    segment.set_image_number(4)
                elif self.segments[i - 1].rect.x >= segment.rect.x and self.segments[i - 1].rect.y <= segment.rect.y and \
                        self.segments[i + 1].rect.y <= segment.rect.y and self.segments[i + 1].rect.x >= segment.rect.x:
                    segment.set_image_number(5)

                if abs(segment.rect.x - self.segments[i - 1].rect.x) > self.game.tile_size or abs(segment.rect.x - self.segments[i + 1].rect.x) > self.game.tile_size:
                    segment.image = pygame.transform.flip(segment.image, True, False)
                elif abs(segment.rect.y - self.segments[i - 1].rect.y) > self.game.tile_size or abs(segment.rect.y - self.segments[i + 1].rect.y) > self.game.tile_size:
                    segment.image = pygame.transform.flip(segment.image, False, True)

            segment.segment_mask_surface = segment.update_segment_mask()

    def get_segment_by_pos(self, x, y):
        for segment in self.segments:
            if segment.rect.x == x and segment.rect.y == y:
                return segment

        return None

    def get_new_segment_pos(self):
        """Returns the x and y coordinates of a tile where new segment should be added. This is determined by position
        of last 2 segments - the returned position must be always in line with the last 2 segments"""

        penultimate_segment = self.segments[len(self.segments) - 2].rect
        last_segment = self.segments[len(self.segments) - 1].rect

        # new segment should be added on the left of last segment
        if last_segment.x < penultimate_segment.x and last_segment.y == penultimate_segment.y:
            return (last_segment.x - self.game.tile_size, last_segment.y)
        # new segment should be added on the right of last segment
        elif last_segment.x > penultimate_segment.x and last_segment.y == penultimate_segment.y:
            return (last_segment.x + self.game.tile_size, last_segment.y)
        # new segment should be added above the last segment
        elif last_segment.x == penultimate_segment.x and last_segment.y < penultimate_segment.y:
            return (last_segment.x, last_segment.y - self.game.tile_size)
        # new segment should be added under the last segment
        elif last_segment.x == penultimate_segment.x and last_segment.y > penultimate_segment.y:
            return (last_segment.x, last_segment.y + self.game.tile_size)


class SnakeSegment:
    def __init__(self, x, y, image_number, snake):
        self.snake = snake
        self.image_number = image_number
        self.image = self.update_image()
        self.rect = self.image.get_rect()

        self.segment_mask_surface = self.update_segment_mask()

        self.rect.x = x
        self.rect.y = y

    def set_image_number(self, i_n):
        self.image_number = i_n
        self.image = self.update_image()

    # updates image of the segment based on the image_number attribute
    def update_image(self):
        image = None
        if self.image_number == 0:
            image = self.snake.current_segment_img
        elif self.image_number == 1:
            image = self.snake.current_head_img
        elif self.image_number == 2:
            image = self.snake.current_corner_bottom_right_img
        # creates left-bottom snake corner segment
        elif self.image_number == 3:
            image = pygame.transform.flip(self.snake.current_corner_bottom_right_img, True, False)
        elif self.image_number == 4:
            image = self.snake.current_corner_left_top_img
        # creates top-right snake corner segment
        elif self.image_number == 5:
            image = pygame.transform.flip(self.snake.current_corner_left_top_img, True, False)
        # tail image
        elif self.image_number == 6:
            image = self.snake.current_tail_img

        return image

    def update_segment_mask(self):
        segment_mask = pygame.mask.from_surface(self.image)
        segment_mask.invert()
        segment_mask_surface = segment_mask.to_surface()
        segment_mask_surface.set_colorkey((255, 255, 255))

        return segment_mask_surface

