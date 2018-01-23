#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
from random import randint
from time import ctime,sleep
import math

pygame.init()

# 30 * 30
row = 30
col = 30

# 每个方块宽高都是20px
square_width = 20
screen = pygame.display.set_mode((row * square_width, col * square_width), 0, 32)

# 定义一些颜色
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
deep_sky_blue = (0, 191, 255)
red = (255, 0, 0)

class Boat(object):
    def __init__(self, x, y, direction, boat_length, boat_width, color=deep_sky_blue):
        self.center_x = x
        self.center_y = y
        self.direction = direction
        self.boat_length = boat_length
        self.boat_width = boat_width
        self.color = color
        self.border_width = 1



def draw_boat(screen, boat):
    # 绘制一个圆形
    position = ball.x, ball.y
    radius = square_width / 2
    width = 1
    color = ball.color

    # pygame.draw.circle
    # 原型：pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    # 当不传入width参数的时候，绘制的是一个填充了的圆
    pygame.draw.circle(screen, color, position, radius)



# 移动向量(delta_row, delta_col)
move = (0, 0)

# 追逐者的路径
path = [(0, 0)]


# 计算巨人移动方向的bresenham算法，会以起点（ball1）和终点（ball2）为数据，算出ball1要走的一连串步伐，使其能以一连串步伐走向ball2。
# 每次ball2移动位置，都需要重新调用这个方法一遍来计算步伐
def chase_bresenham(ball1, ball2):
    # 计算移动方向
    delta_row = ball2.current_row_index - ball1.current_row_index
    delta_col = ball2.current_col_index - ball1.current_col_index

    if delta_row == 0 and delta_col == 0:
        return (0, 0)

    if math.fabs(delta_row) > math.fabs(delta_col):
        move = (int(delta_row/math.fabs(delta_row)), 0)
    elif math.fabs(delta_row) < math.fabs(delta_col):
        move = (0, int(delta_col / math.fabs(delta_col)))
    else:
        move = (int(delta_row/math.fabs(delta_row)), int(delta_col / math.fabs(delta_col)))

    return move


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                # 按下的是左方向键的话，把x坐标减一
                move = (0, -1)

            elif event.key == K_RIGHT:
                # 右方向键则加一
                move = (0, 1)

            elif event.key == K_UP:
                move = (-1, 0)

            elif event.key == K_DOWN:
                move = (1, 0)

        elif event.type == KEYUP:
            # 如果用户放开了键盘，图就不要动了
            move = (0, 0)

    # 绘制白色背景色
    screen.fill(white)


    pygame.display.update()
    sleep(0.5)
