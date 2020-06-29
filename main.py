import pygame; from time import sleep
from pygame.sprite import Group, Sprite
from random import choice, randint; import sys

def update_x_y(length, xs, ys, snake):
    while len(xs)<=length:
        xs.append(snake.rect.centerx)
        ys.append(snake.rect.centery)
    xs.remove(xs[0]); ys.remove(ys[0])
    return xs, ys

def new_apple_pos(apple, xs, ys):
    avlbl = []
    for i in range(25, 1200, 50):
        for j in range(25, 600, 50):
            avlbl.append((i, j))
    pos = []
    for i in range(len(xs)):
        pos.append((xs[i], ys[i]))
    while True:
        x, y = choice(avlbl)
        if (x, y) not in pos:
            apple.rect.centerx=x
            apple.rect.centery=y
            break

def check_apple_coll(snake, apple, snake_cells, screen, settings, length, xs, ys):
    if snake.rect.centerx==apple.rect.centerx and snake.rect.centery==apple.rect.centery:
        length += 1; xs, ys = update_x_y(length, xs, ys, snake)
        snake_cells.add(SnakeCell(screen, apple, settings, xs, ys))
        new_apple_pos(apple, xs, ys)
    return length, xs, ys

def update_screen(snake, apple, snake_cells, screen, settings, xs, ys, pButton):
    screen.fill(settings.screen_color)
    if not settings.active:
        pButton.draw_button()
    else:
        apple.draw_apple()
        snake.move()
        for i in range(len(snake_cells.sprites())):
            snake_cells.sprites()[i].update(xs[i+1], ys[i+1])
        check_border(snake)
        snake.draw_snake()
    pygame.display.flip()

def check_border(snake):
    if snake.rect.centerx<0:
        snake.rect.centerx=1175
    elif snake.rect.centerx>1200:
        snake.rect.centerx=25
    if snake.rect.centery<0:
        snake.rect.centery=575
    elif snake.rect.centery>600:
        snake.rect.centery=25

def check_button(settings, pButton, x, y):
    if pButton.rect.collidepoint(x, y) and not settings.active:
        settings.active = True

def check_click(snake, settings, pButton):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not snake.moving_left:
                snake.moving_right = True
                snake.moving_left = False
                snake.moving_up = False
                snake.moving_down = False
            elif event.key == pygame.K_LEFT and not snake.moving_right:
                snake.moving_right = False
                snake.moving_left = True
                snake.moving_up = False
                snake.moving_down = False
            elif event.key == pygame.K_UP and not snake.moving_down:
                snake.moving_right = False
                snake.moving_left = False
                snake.moving_up = True
                snake.moving_down = False
            elif event.key == pygame.K_DOWN and not snake.moving_up:
                snake.moving_right = False
                snake.moving_left = False
                snake.moving_up = False
                snake.moving_down = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button(settings, pButton, mouse_x, mouse_y)


class Apple:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(0, 0, self.settings.apple_width,
                                self.settings.apple_height)
        self.rect.centerx, self.rect.centery = self.set_rect()
        self.color = self.settings.apple_color

    def set_rect(self):
        x = randint(1, (self.settings.screen_width/50))*50 - 25
        y = randint(1, (self.settings.screen_height/50))*50 - 25
        return x, y

    def draw_apple(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Snake_body:
    def __init__(self, screen, settings, apple):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(0, 0, self.settings.snake_width,
                                self.settings.snake_height)
        self.color = self.settings.snake_color
        self.rect.centerx, self.rect.centery = self.set_pos(apple)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def move(self):
        if self.moving_right:
            self.rect.centerx += 50
        if self.moving_left:
            self.rect.centerx -= 50
        if self.moving_up:
            self.rect.centery -= 50
        if self.moving_down:
            self.rect.centery += 50

    def set_pos(self, apple):
        x = apple.rect.centerx
        y = apple.rect.centery
        while x == apple.rect.centerx:
            x = randint(1, (self.settings.screen_width/50))*50 - 25
        while y == apple.rect.centery:
            y = randint(1, (self.settings.screen_height/50))*50 - 25
        return x, y

    def draw_snake(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Settings():
    def __init__(self):
        self.active = False

        self.screen_height = 600
        self.screen_width = 1200
        self.screen_color = (0, 250, 0)

        self.apple_color = (250, 0, 0)
        self.apple_width = 50
        self.apple_height = 50

        self.snake_color = (0, 0, 0)
        self.snake_width = 50
        self.snake_height = 50

class SnakeCell(Sprite):
    def __init__(self, screen, apple, settings, xs, ys):
        super(SnakeCell, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.snake_width,
                                settings.snake_height)
        self.rect.centerx, self.rect.centery = xs[len(xs)-1], ys[len(ys)-1]
        self.color = settings.snake_color
        self.draw_snake()

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.draw_snake()

    def draw_snake(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Button():
    def __init__(self, screen, settings, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))

    pButton = Button(screen, settings, "Zagraj")
    xs, ys = [], []; length = 1
    apple = Apple(screen, settings)
    snake = Snake_body(screen, settings, apple)
    xs.append(snake.rect.centerx); ys.append(snake.rect.centery)
    snake_cells = Group()
    pygame.display.set_caption("snakes")
    update_screen(snake, apple, snake_cells, screen, settings, xs, ys, pButton)

    while True:
        xs, ys = update_x_y(length, xs, ys, snake)
        check_click(snake, settings, pButton)
        if settings.active:
            length, xs, ys = check_apple_coll(snake, apple, snake_cells, screen, settings, length, xs, ys)
            update_screen(snake, apple, snake_cells, screen, settings, xs, ys, pButton)
            if pygame.sprite.spritecollideany(snake, snake_cells):
                lButton = Button(screen, settings, "Koniec gry")
                lButton.draw_button()
                pygame.display.flip()
                sleep(3)
                break
            sleep(0.15)

    pygame.quit()

if __name__=='__main__':
    run_game()
