import math
from random import choice, randrange, random

import pygame

#1. Избавиться от global
#2. docstring к каждому методу
#3. форматировать black .\classwork10\gun_final2.py
#4. Прописать документацию к переменным
#5. Написать class gamelead - командует всеми остальными объектами
FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Gamelead:
    pass
class Ball:
    def __init__(self, screen: pygame.Surface, x=20, y=450):
        """Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= 1  # gravity
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r > WIDTH:  # check vertical wall
            self.vx = (-self.vx) * 0.5  # 0.5 means friction effect
            self.vy = self.vy * 0.5
            self.x = WIDTH - self.r
        if self.y + self.r > HEIGHT:  # check horizontal wall
            self.vy = -self.vy * 0.5
            self.vx = self.vx * 0.5
            self.y = HEIGHT - self.r

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r,
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Cball(Ball):
    def __init__(self, screen, x=20, y=450, vx=0, vy=0):
        super().__init__(screen, x, y)
        self.vx = vx
        self.vy = vy
        self.r = 5
        self.color = BLACK

    def move(self):
        self.x += self.vx
        self.y -= self.vy
    def draw(self):
        super().draw()
    def hittest(self, obj):
        return super().hittest(obj)


class Gun:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power: int = 10
        self.f2_on = 0
        self.an: int = 1
        self.a: int = 20  # big side
        self.b: int = 5  # short side
        self.color: int = GREY
        self.x: int = 20 #coord of gun
        self.v: int = 0 #velocity

    def fire2_start(self, event):
        self.f2_on = 1

    def fire1(self):
        '''Выстрел cball'''
        global balls, bullet
        bullet += 1
        new_cball = Cball(self.screen, vx=math.cos(self.an), vy=-math.sin(self.an), x=self.x)
        balls.append(new_cball)

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x=self.x)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.a = 20

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1] - 450), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.polygon(
            self.screen,
            self.color,
            (
                (self.x, 450),
                (self.x + self.a * math.cos(self.an), 450 + self.a * math.sin(self.an)),
                (
                    self.x + self.a * math.cos(self.an) + self.b * math.sin(self.an),
                    450 + self.a * math.sin(self.an) - self.b * math.cos(self.an),
                ),
                (self.x + self.b * math.sin(self.an), 450 - self.b * math.cos(self.an)),
            ),
        )

    def power_up(self):
        '''Процесс зарядки пушки. Тик каждый кадр'''
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.a += 1
            self.color = RED
        else:
            self.color = GREY
    
    def move(self):
        self.x += self.v



class Target:
    def __init__(self, screen: pygame.Surface, color=RED, vx=0):
        self.x = randrange(600, 780)
        self.y = randrange(300, 550)
        self.r = randrange(10, 50)
        self.v = random() * choice((-1, 1))
        self.vx = vx
        self.color = color
        self.screen = screen
        self.points = 0
        self.live = 1

    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """Инициализация новой цели."""
        pass

    def move(self):
        '''Движение цели. Логика столкновений'''
        self.y += self.v
        self.x += self.vx

        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.v = -self.v
        elif self.y - self.r <= 0:
            self.y = self.r
            self.v = -self.v
        elif self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        elif self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global counter, bullet
        self.points += points
        counter += 1
        text = font.render("Вы поразили мишени за " + str(bullet) + " выстрелов.", True, BLACK)
        bullet = 0
        self.screen.blit(text, [150, 200])
        pygame.display.flip()
        clock.tick(1)

    def draw(self):
        if self.live:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        else:
            pass

    def hittest(self, obj):
        '''Есть ли столкновение?'''
        if (self.x - obj.x)**2 + (self.y-obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


pygame.init()
font = pygame.font.Font("freesansbold.ttf", 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
counter = 0
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target_easy = Target(screen)
target_hard = Target(screen, color=GREEN, vx=randrange(-5, 5))
while target_easy.hittest(target_hard):
    target_easy = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    TEXT = font.render(str(counter), True, BLACK)
    screen.blit(TEXT, [10, 10])
    gun.draw()
    target_easy.draw()
    target_hard.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            gun.fire1()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            gun.v = 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            gun.v = -3
        elif event.type == pygame.KEYUP and (event.key == pygame.K_LEFT):
            gun.v = 0
        elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT):
            gun.v = 0

    for b in balls:
        b.move()
        if abs(b.vx) <= 0.001:
            balls.remove(b)
        if b.hittest(target_easy) and target_easy.live:
            target_easy.live = 0
        if b.hittest(target_hard) and target_hard.live:
            target_hard.live = 0
        if not target_easy.live and not target_hard.live:
            balls.clear()
            target_easy.hit()
            target_easy = Target(screen)
            target_hard = Target(screen, color=GREEN, vx=randrange(-5, 5))
            while target_easy.hittest(target_hard):
                target_easy = Target(screen)

    gun.power_up()
    gun.move()
    target_easy.move()
    target_hard.move()

pygame.quit()
