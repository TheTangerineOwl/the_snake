"""Игра "Более крутая змейка"."""

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

GRID_CENTER_X = GRID_WIDTH // 2
GRID_CENTER_Y = GRID_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 64, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)
BAD_APPLE_COLOR = (200, 172, 64)
STONE_COLOR = (172, 172, 172)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

SNAKE_HEAD_COLOR = (0, 128, 0)

DEFAULT_COLOR = (255, 255, 255)
DEFAULT_POSITION = (0, 0)

# Скорость движения змейки (по умолчанию 20):
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Описывает стандартный объект игры."""

    def __init__(
            self,
            position=DEFAULT_POSITION,
            body_color=DEFAULT_COLOR
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки игрового объекта."""
        pass


class Apple(GameObject):
    """Описывает объект яблока."""

    def __init__(
            self,
            body_color=APPLE_COLOR
    ):
        super().__init__(
            position=self.randomize_position(),
            body_color=body_color
        )

    def randomize_position(self):
        """Задает яблоку случайную позицию на игровом поле."""
        x_coord = randint(0, (GRID_WIDTH - 1)) * GRID_SIZE
        y_coord = randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        self.position = (x_coord, y_coord)
        return self.position

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class BadApple(Apple):
    """Описывает объект "плохого" яблока."""

    def __init__(self):
        super().__init__(
            body_color=BAD_APPLE_COLOR
        )


class Stone(GameObject):
    """Описывает объект камня."""

    def __init__(
            self,
            body_color=STONE_COLOR
    ):
        self.position = self.randomize_position()
        self.body_color = body_color

    def randomize_position(self):
        """Задает случайную позицию на игровом поле."""
        x_coord = randint(0, (GRID_WIDTH - 1)) * GRID_SIZE
        y_coord = randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        self.position = (x_coord, y_coord)
        return self.position

    def draw(self):
        """Отрисовывает камень на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает объект змейки."""

    def __init__(
            self,
            length=1,
            positions=[(GRID_CENTER_X * GRID_SIZE,
                        GRID_CENTER_Y * GRID_SIZE)],
            direction=RIGHT,
            next_direction=None,
            body_color=SNAKE_COLOR
    ):
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.last = None
        super().__init__(position=positions[0],
                         body_color=body_color)

    def update_direction(self):
        """Обновление направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки вперед в направлении direction."""
        old_head = self.get_head_position()
        new_head_x = (old_head[0] + self.direction[0] * GRID_SIZE) \
            % (GRID_WIDTH * GRID_SIZE)
        new_head_y = (old_head[1] + self.direction[1] * GRID_SIZE) \
            % (GRID_HEIGHT * GRID_SIZE)
        self.position = (new_head_x, new_head_y)
        self.positions.insert(0, self.position)
        self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        # for position in self.positions[:-1]:
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        # return self.positions[0]
        return self.position

    def reset(self):
        """Возвращает змейку в начальную позицию после поражения."""
        self.length = 1
        self.positions = [(GRID_CENTER_X * GRID_SIZE,
                           GRID_CENTER_Y * GRID_SIZE)]
        self.direction = choice([RIGHT, DOWN, LEFT, UP])
        self.next_direction = None
        self.position = self.positions[0]
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обработка действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игрового процесса."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    bad_apple = BadApple()
    stone = Stone()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            bad_apple.randomize_position()
            stone.randomize_position()
            snake.length += 1
            snake.positions.append(snake.last)
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == bad_apple.position:
            apple.randomize_position()
            bad_apple.randomize_position()
            stone.randomize_position()
            snake.length -= 1
            if snake.last:
                last_rect = pygame.Rect(snake.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            if snake.length < 1:
                snake.reset()
            else:
                snake.last = snake.positions.pop()
                screen.fill(BOARD_BACKGROUND_COLOR)
        if len(set(snake.positions)) != snake.length \
           or snake.get_head_position() == stone.position:
            snake.reset()
            apple.randomize_position()
            bad_apple.randomize_position()
            stone.randomize_position()
        snake.draw()
        apple.draw()
        bad_apple.draw()
        stone.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN
#                  and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT
#                  and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#                  and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
