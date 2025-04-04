import pygame
import random

class Snake:
    def __init__(self, pos, walls):
        # Инициализация змейки с начальной позицией и стенами
        self.pos = pos  # Позиции змейки
        self.possible_possition = [(i, j) for i in range(34) for j in range(24)]  # Все возможные позиции на игровом поле
        self.possible_possition.append((-1, -1))  # Добавляем специальную позицию для удалённого сегмента змейки
        self.time = 0  # Счётчик времени
        
        # Убираем стартовые позиции змейки и стены из списка возможных позиций
        for i in pos:
            self.possible_possition.remove(i)
        for i in walls:
            self.possible_possition.remove(i)

    def move(self, direct):
        # Движение змейки в указанном направлении
        if direct == 0:
            self.pos.insert(0, (self.pos[0][0]+1, self.pos[0][1]))  # Движение вправо
        elif direct == 1:
            self.pos.insert(0, (self.pos[0][0], self.pos[0][1]+1))  # Движение вниз
        elif direct == 2:
            self.pos.insert(0, (self.pos[0][0]-1, self.pos[0][1]))  # Движение влево
        else:
            self.pos.insert(0, (self.pos[0][0], self.pos[0][1]-1))  # Движение вверх
        
        try:
            self.possible_possition.remove(self.pos[0])  # Удаляем новую голову из списка возможных позиций
        except:
            return True  # Если произошло столкновение, возвращаем True
        
        self.possible_possition.append(self.pos[-1])  # Добавляем старый хвост обратно в список возможных позиций
        self.pos.pop()  # Удаляем старый хвост

    def eat(self, a, s, t):
        # Функция, обрабатывающая поедание яблока
        self.time += 1  # Увеличиваем счётчик времени
        if self.pos[0][0] == a[0] and self.pos[0][1] == a[1] or self.time > 30:  # Если змейка съела яблоко или прошло 30 ходов
            self.possible_possition.remove((-1, -1))  # Удаляем специальную позицию из списка возможных позиций
            a = random.choice(self.possible_possition)  # Выбираем новую случайную позицию для яблока
            if self.time > 30:  # Если прошло более 30 ходов
                self.possible_possition.append((-1, -1))  # Добавляем специальную позицию обратно в список возможных
            else:
                self.pos.append((-1, -1))  # Добавляем новый сегмент змейки
                s += t  # Увеличиваем счёт
            self.time = 0  # Сбрасываем счётчик времени
            t = random.randint(1, 3)  # Генерируем новый случайный тип фрукта
        return a, s, t  # Возвращаем новую позицию яблока, счёт и тип фрукта

    def draw(self, window):
        # Отрисовка змейки на игровом окне
        for i in range(len(self.pos)):
            pygame.draw.rect(window, (0, 255, 0), (self.pos[i][0]*25, self.pos[i][1]*25, 25, 25))  # Отрисовываем каждый сегмент змейки
