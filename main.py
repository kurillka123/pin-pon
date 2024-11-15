import pygame

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 300

class Game:
    def __init__(self) -> None:
        pygame.init()
        display_info = pygame.display.Info() # экземпляр класса Info
        self.window_width = display_info.current_w # атрибуты Info (ширина)
        self.window_height = display_info.current_h # атрибуты Info (высота)
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        
        # левая ракетка
        x_left = self.window_width // 10
        self.racket_left = Racket(
            x_left, 
            self
            )
        
        # правая ракетка
        x_right = self.window_width // 10 * 9 - Racket.width
        self.racket_right = Racket(
            x_right,
            self
            )
        
        # мяч
        self.ball = Ball(
            self
            )
        
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.main_loop()

    def main_loop(self) -> None:
        while self.is_running:
            '''
            сбор событий
            изменения (обьектов)
            рендер (отрисовка)
            ожидание FPS
            '''
            self.handle_events() # вызов функции handle_events
            self.update() # вызов функции update
            self.render() # вызов функции render
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self) -> None:
        '''обрабатывает события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.racket_right.move(0, -1)
                if event.key == pygame.K_DOWN:
                    self.racket_right.move(0, 1)
                if event.key == pygame.K_w:
                    self.racket_left.move(0, -1)
                if event.key == pygame.K_s:
                    self.racket_left.move(0, 1)
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                    
    def update(self) -> None:
        self.ball.update()
        self.racket_left.update()
        self.racket_right.update()



    def render(self):
        '''отрисовывает обьекты на екране'''
        self.screen.fill(BLACK)
        self.racket_left.render()
        self.racket_right.render()
        self.ball.render()
        pygame.display.flip()


class Ball:
    width = 20
    height = 20

    def __init__(self,game: Game) -> None:
        self.color = WHITE
        self.speed = 2
        self.velocity_x = 1
        self.velocity_y = 0
        self.rect = pygame.Rect(0, 0, Ball.width, Ball.height)
        self.game = game
        self.goto_start()

    def goto_start(self):
        self.rect.centerx = self.game.window_width // 2
        self.rect.centery = self.game.window_height // 2

    def move(self) -> None:
        self.rect.x += self.velocity_x * self.speed
        self.rect.y += self.velocity_y * self.speed

    def collide_barders(self) -> None:
        '''столкновение с экраном'''
        if self.rect.right >= self.game.window_width:
            self.velocity_x *= -1
        elif self.rect.left <= 0:
            self.velocity_x *= -1
        elif self.rect.top <= 0:
            self.velocity_y *= -1
        elif self.rect.bottom >= self.game.window_height:
            self.velocity_y *= -1

    def collide_rackets(self):
        '''столкновение с ракетками'''
        if self.rect.colliderect(self.game.racket_left.rect):
            self.velocity_x *= -1
        elif self.rect.colliderect(self.game.racket_right.rect):
            self.velocity_x *= -1
            

    def render(self) -> None:
        pygame.draw.rect(self.game.screen, self.color, self.rect, 0)

    def update(self) -> None:
        self.move()
        self.collide_barders()
        self.collide_rackets()



class Racket:

    width = 40
    height = 250
    def __init__(self, center_x: int, game: Game):
        self.center_x = center_x
        self.color = WHITE
        self.speed = 30
        self.rect = pygame.Rect(0, 0, Racket.width,  Racket.height)
        self.game = game
        self.goto_start()

    def goto_start(self):
        self.rect.centerx = self.center_x
        self.rect.centery = self.game.window_height // 2

    def move(self, x: int, y: int):
        '''двигает ракетку'''
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed
        self.rect.topleft = (self.rect.x, self.rect.y)

    def collide_borders(self):
        if self.rect.bottom > self.game.window_height:
            self.rect.bottom = self.game.window_height
        elif self.rect.top < 0:
            self.rect.top = 0

    def render(self):
        '''рисует ракетку'''
        pygame.draw.rect(self.game.screen, self.color,self.rect, 0)

    def update(self):
        self.collide_borders()





Game()