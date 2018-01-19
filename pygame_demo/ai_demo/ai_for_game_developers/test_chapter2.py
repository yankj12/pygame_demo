#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
from random import randint

pygame.init()

# 15 * 15
row = 15
col = 15

# 每个方块宽高都是20px
square_width = 20
screen = pygame.display.set_mode((row * square_width, col * square_width), 0, 32)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
deep_sky_blue = (0, 191, 255)
red = (255, 0, 0)

class Ball(object):
    def __init__(self, row_index, col_index, color=white):
        self.current_row_index = row_index
        self.current_col_index = col_index
        self.color = color
        self.x = self.current_row_index * square_width + square_width / 2
        self.y = self.current_col_index * square_width + square_width / 2
        self.radius = square_width / 2

    def update(self, move=(0,0)):
        self.current_row_index += move[0]
        self.current_col_index += move[1]

        self.current_row_index = self.current_row_index%row
        self.current_col_index = self.current_col_index%col

        self.x = self.current_row_index * square_width + square_width / 2
        self.y = self.current_col_index * square_width + square_width / 2


def draw_ball(screen, ball):
    # 绘制一个圆形
    position = ball.x, ball.y
    radius = square_width / 2
    width = 1
    color = ball.color

    # pygame.draw.circle
    # 原型：pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    # 当不传入width参数的时候，绘制的是一个填充了的圆
    pygame.draw.circle(screen, color, position, radius)

#球1是追踪者
row_index1 = randint(0, 14)
col_index1 = randint(0, 14)
ball1 = Ball(row_index1, col_index1)
#球2是目标
row_index2 = randint(0, 14)
col_index2 = randint(0, 14)
ball2 = Ball(row_index2, col_index2, red)

move = (0, 0)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                # 按下的是左方向键的话，把x坐标减一
                move = (-1, 0)
                ball2.update(move)
            elif event.key == K_RIGHT:
                # 右方向键则加一
                move = (1, 0)
                ball2.update(move)
            elif event.key == K_UP:
                move = (0, -1)
                ball2.update(move)
            elif event.key == K_DOWN:
                move = (0, 1)
                ball2.update(move)
        elif event.type == KEYUP:
            # 如果用户放开了键盘，图就不要动了
            move = (0, 0)

    # 绘制黑色背景色
    screen.fill(deep_sky_blue)
    # 绘制白色方格线
    for r in range(0 , row + 1):
        pygame.draw.aaline(screen, black, (0, r * square_width), (col * square_width, r * square_width))

    for c in range(0, col + 1):
        pygame.draw.aaline(screen, black, (c * square_width, 0), (c * square_width, col * square_width))


    # 绘制两个小球
    draw_ball(screen, ball1)
    draw_ball(screen, ball2)

    pygame.display.update()