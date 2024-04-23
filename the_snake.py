from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Счетчик
WHITE = (255, 255, 255)
FONT_SIZE = 24

# Шрифт
font = pg.font.Font(None, FONT_SIZE)

# Клавиши
TURNS = {(pg.K_UP, DOWN): UP,
         (pg.K_DOWN, UP): DOWN,
         (pg.K_LEFT, RIGHT): LEFT,
         (pg.K_RIGHT, LEFT): RIGHT}


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие"""

    def __init__(self, body_color: tuple = None) -> None:
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = body_color

    def draw(self) -> None:
        """Метод для отрисовки объекта на игровом поле"""
        raise NotImplementedError()

    @staticmethod
    def draw_square(position: tuple, color: tuple) -> None:
        """Метод для отрисовки квадратов"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывабщий блоко и действия с ним"""

    def __init__(self) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Случайное положение яблока."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Отрисовка яблока"""
        self.draw_square(self.position, self.body_color)


class Snake(GameObject):
    """
    Класс змеи, содержит атрибуты и методы класса обеспечивабщий логику
    движения, отрисовки, обработки событий и другие аспекты.
    """

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self) -> None:
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки"""
        head = self.get_head_position()

        dx, dy = self.direction
        new = (((head[0] + (dx * GRID_SIZE)) % SCREEN_WIDTH),
               ((head[1] + (dy * GRID_SIZE)) % SCREEN_HEIGHT))

        if new in self.positions:
            self.reset()
        else:
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop()
            self.positions.insert(0, new)

    def draw(self) -> None:
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            self.draw_square(position, self.body_color)

        # Отрисовка головы змейки
        self.draw_square(self.positions[0], self.body_color)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Позиция головы змейки"""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывание змейки в начальное состояние"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            for key, direction in TURNS:
                if event.key == key and game_object.direction != direction:
                    game_object.next_direction = TURNS[(key, direction)]


def main():
    """Основной цикл игры"""
    snake = Snake()
    apple = Apple()

    # Создайте текстовый объект
    score = 0
    score_text = font.render(f"Score: {score}", True, WHITE)

    # Позиция текста
    score_rect = score_text.get_rect(top=10,
                                     centerx=SCREEN_WIDTH // 2)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        # Если местоположение совпадает пересоздаем яблоко
        if apple.position in snake.positions[1::]:
            apple.randomize_position()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        score = snake.length
        score_text = font.render(f"Score: {score}", True, WHITE)

        apple.draw()
        snake.draw()

        screen.blit(score_text, score_rect)

        pg.display.update()


if __name__ == '__main__':
    main()
