# Импортирование библиотек
import pygame
import sys
import random
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Создание окна для игры
window = pygame.display.set_mode((840, 600))

# Установка заголовка окна
pygame.display.set_caption("Game")

# Загрузка изображения дороги
road = pygame.image.load('Lab_8/img/road.png')

# Установка частоты кадров (FPS)
FPS = 60
FramePerSec = pygame.time.Clock()

# Начальная скорость
speed = 2

# Определение цветов (черный, красный, белый, желтый)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Шрифты для текста
font = pygame.font.SysFont("Verdana", 100)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка изображения монеты
coin = pygame.image.load('Lab_8/img/coin.png')
coin.set_colorkey(WHITE)  # Убираем белый цвет из изображения
coin = pygame.transform.scale(coin, (20, 20))  # Масштабируем монету

# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Загрузка изображения машины игрока
        self.image = pygame.image.load('Lab_8/img/car1.png')
        self.image.set_colorkey((255, 255, 255))  # Убираем белый цвет
        self.image = pygame.transform.rotate(self.image, 90)  # Поворот на 90 градусов
        self.image = pygame.transform.scale(self.image, (102, 150))  # Масштабируем изображение
        self.rect = self.image.get_rect()  # Получаем прямоугольник, который описывает объект
        self.rect.x = x  # Устанавливаем начальную позицию по оси X
        self.rect.y = y  # Устанавливаем начальную позицию по оси Y
    
    # Обновление позиции игрока
    def update(self, score):
        fail = False
        keys = pygame.key.get_pressed()  # Получаем состояние клавиш

        # Управление движением игрока
        if keys[pygame.K_a] and self.rect.x > 140:  # Если нажата клавиша 'A' (влево)
            self.rect.x -= 3 * speed
        if keys[pygame.K_d] and self.rect.x < 605:  # Если нажата клавиша 'D' (вправо)
            self.rect.x += 3 * speed

        # Проверка на столкновение с машинами
        if pygame.sprite.spritecollide(self, cars, False):
            fail = True  # Если столкновение с машиной, игра заканчивается
        # Проверка на столкновение с монетами
        if pygame.sprite.spritecollide(self, coins, False):
            coin_in_road.rect.y = -200  # Перемещаем монету за пределы экрана
            lines = [190, 320, 440, 570]  # Возможные координаты для новой монеты
            line = random.randint(0, 3)  # Выбираем случайную позицию
            coin_in_road.rect.x = lines[line]  # Устанавливаем новую позицию монеты
            score += random.randint(1, 5)  # Увеличиваем счет случайным числом от 1 до 5
        
        return fail, score
    
    # Отображение игрока на экране
    def draw(self):
        window.blit(self.image, self.rect)

# Класс для машин противников
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Загрузка изображения машины противника
        self.image = pygame.image.load('Lab_8/img/car2.png')
        self.image.set_colorkey((255, 255, 255))  # Убираем белый цвет
        self.image = pygame.transform.rotate(self.image, 270)  # Поворот на 270 градусов
        self.image = pygame.transform.scale(self.image, (100, 150))  # Масштабируем изображение
        self.rect = self.image.get_rect()  # Получаем прямоугольник, который описывает объект
        self.rect.x = x  # Устанавливаем начальную позицию по оси X
        self.rect.y = y  # Устанавливаем начальную позицию по оси Y

    # Обновление позиции машины
    def update(self):
        lines = [180, 300, 440, 570]  # Возможные позиции по оси X
        self.rect.y += 2 * speed  # Машина двигается вниз
        line = random.randint(0, 3)  # Выбираем случайную позицию по оси X
        if self.rect.y > 800:  # Если машина вышла за пределы экрана
            self.rect.y = -300  # Перемещаем машину в начало
            self.rect.x = lines[line]  # Устанавливаем случайную позицию по оси X
    
    # Отображение машины на экране
    def draw(self):
        window.blit(self.image, self.rect)

# Класс для монет
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Загрузка изображения монеты
        self.image = pygame.image.load('Lab_8/img/coin.png')
        self.image.set_colorkey(WHITE)  # Убираем белый цвет
        self.image = pygame.transform.scale(self.image, (75, 75))  # Масштабируем монету
        self.rect = self.image.get_rect()  # Получаем прямоугольник, который описывает объект
        self.rect.x = x  # Устанавливаем начальную позицию по оси X
        self.rect.y = y  # Устанавливаем начальную позицию по оси Y
    
    # Обновление позиции монеты
    def update(self):
        lines = [190, 320, 440, 570]  # Возможные позиции по оси X
        self.rect.y += 2 * speed  # Монета двигается вниз
        line = random.randint(0, 3)  # Выбираем случайную позицию по оси X
        if self.rect.y > 700:  # Если монета вышла за пределы экрана
            self.rect.y = -200  # Перемещаем монету за экран
            self.rect.x = lines[line]  # Устанавливаем случайную позицию по оси X
        if pygame.sprite.spritecollide(self, cars, False):  # Если монета столкнулась с машиной
            self.rect.y = -200  # Перемещаем монету за пределы экрана
            self.rect.x = lines[line]  # Устанавливаем новую позицию по оси X
    
    # Отображение монеты на экране
    def draw(self):
        window.blit(self.image, self.rect)

# Создание экземпляра игрока
player = Player(180, 430)

# Создание групп для машин и монет
cars = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Создание монеты на дороге
coin_in_road = Coin(190, -100)
coins.add(coin_in_road)

# Создание машин противников
for i in range(2):
    car = Car(570, 130)
    cars.add(car)
    car = Car(570, -330)
    cars.add(car)

# Начальные координаты для движения дороги
y1 = 0
y2 = -600

# Переменная для завершения игры
fail = False

# Начальный счёт
score = 0

# Главный игровой цикл
while not fail:
    window.fill((0, 0, 0))  # Заполнение экрана черным
    window.blit(road, (0, y1))  # Отображение первой дороги
    window.blit(road, (0, y2))  # Отображение второй дороги

    score_txt = font_small.render(str(score), True, YELLOW)  # Отображение счёта
    window.blit(score_txt, (50, 50))
    window.blit(coin, (20, 52))  # Отображение монеты

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если окно закрыто
            pygame.quit()
            sys.exit()

    # Движение дороги
    y1 += speed
    y2 += speed
    if y1 >= 600:
        y1 -= 1200  # Перемещаем первую дорогу обратно
    elif y2 >= 600:
        y2 -= 1200  # Перемещаем вторую дорогу обратно

    # Обновление и отрисовка машин
    for i in cars:
        i.update()
        i.draw()

    # Обновление и отрисовка монеты
    coin_in_road.update()
    coin_in_road.draw()

    # Обновление игрока
    fail, score = player.update(score)
    player.draw()

    pygame.display.update()  # Обновление экрана
    FramePerSec.tick(FPS)  # Поддержание заданной частоты кадров

# Обработка завершения игры
while fail:
    window.fill(RED)  # Заполнение экрана красным
    window.blit(game_over, (150, 250))  # Отображение текста "Game Over"

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
