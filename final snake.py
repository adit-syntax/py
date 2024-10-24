import pygame
import random
from functools import reduce

pygame.init()
width = 800
height = 600
snake_size = 20
fps = 15


def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"Action performed: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def food_generator():
    while True:
        yield (random.randint(0, (width - snake_size) // snake_size) * snake_size,
               random.randint(0, (height - snake_size) // snake_size) * snake_size)


class MoveObject:
    def __init__(self, position):
        self.position = position

    def move(self):
        pass


class Snake(MoveObject):
    speed = 1

    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (snake_size, 0)
        self.grow = False
        super().__init__(self.body[0])

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def change_direction(self, direction):
        if direction == 'UP':
            self.direction = (0, -snake_size)
        elif direction == 'DOWN':
            self.direction = (0, snake_size)
        elif direction == 'LEFT':
            self.direction = (-snake_size, 0)
        elif direction == 'RIGHT':
            self.direction = (snake_size, 0)

    @log_action
    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def grow_snake(self):
        self.grow = True

    def display(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (segment[0], segment[1], snake_size, snake_size))

    @staticmethod
    def check_collision(pos1, pos2):
        return pos1 == pos2


class Food(MoveObject):
    def __init__(self, generator):
        self.position = next(generator)
        super().__init__(self.position)

    @log_action
    def respawn(self, generator):
        self.position = next(generator)

    def display(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.position[0], self.position[1], snake_size, snake_size))


class Game:
    high_scores = []

    def __init__(self):
        self.snake = Snake()
        self.food_generator = food_generator()
        self.food = Food(self.food_generator)
        self.score = 0
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')

    @log_action
    def update_game(self):
        self.snake.move()
        if Snake.check_collision(self.snake.body[0], self.food.position):
            self.snake.grow_snake()
            self.food.respawn(self.food_generator)
            self.score += 1
            Game.update_high_score(self.score)

        if self.snake.body[0][0] < 0 or self.snake.body[0][0] >= width or self.snake.body[0][1] < 0 or \
                self.snake.body[0][1] >= height or self.snake.body[0] in self.snake.body[1:]:
            self.is_running = False

    def draw(self):
        surface = pygame.display.set_mode((width, height))
        surface.fill((0, 0, 0))

        self.snake.display(surface)
        self.food.display(surface)

        pygame.display.flip()

    @classmethod
    def update_high_score(cls, score):
        cls.high_scores.append(score)
        cls.high_scores = sorted(cls.high_scores, reverse=True)[:5]

    @staticmethod
    def get_average_score():
        return reduce(lambda x, y: x + y, Game.high_scores) / len(Game.high_scores) if Game.high_scores else 0

    @staticmethod
    def get_even_scores():
        return list(filter(lambda x: x % 2 == 0, Game.high_scores))


if __name__ == "__main__":
    game = Game()

    clock = pygame.time.Clock()

    while game.is_running:
        game.handle_events()
        game.update_game()
        game.draw()
        clock.tick(fps)

    print("High Scores:", Game.high_scores)
    print("Average Score:", Game.get_average_score())
    print("Even Scores:", Game.get_even_scores())

    pygame.quit()
