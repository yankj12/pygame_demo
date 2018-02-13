#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random

class PathPoint(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col


class AiEntity(object):

    def __init__(self, k_max_rows, k_max_cols):
        self.k_max_rows = k_max_rows
        self.k_max_cols = k_max_cols
        # self.pattern = [[0] * self.k_max_cols] * self.k_max_rows    # 这种初始化方式始终浅层复制的方式，在此例中不符合应用要求
        self.pattern = []
        for i in range(0, self.k_max_rows, 1):
            ary = []
            for j in range(0, self.k_max_cols, 1):
                ary.append(0)
            self.pattern.append(ary)


    # 初始化路径
    def initialize_path_array(self):
        for i in range(0, self.k_max_rows, 1):
            for j in range(0, self.k_max_cols, 1):
                self.pattern[i][j] = 0


    # 向模式数组中添加环节，段落
    def build_path_segment(self, start_point, end_point):
        current_point = PathPoint(start_point.row, start_point.col)
        self.pattern[current_point.row][current_point.col] = 1
        delta_row = end_point.row - current_point.row
        delta_col = end_point.col - current_point.col

        while delta_row != 0 or delta_col != 0:
            if math.fabs(delta_row) > math.fabs(delta_col):
                next_row = current_point.row + int(delta_row / math.fabs(delta_row))
                next_col = current_point.col
            elif math.fabs(delta_row) == math.fabs(delta_col):
                next_row = current_point.row + int(delta_row / math.fabs(delta_row))
                next_col = current_point.col + int(delta_col / math.fabs(delta_col))
            else:
                next_row = current_point.row
                next_col = current_point.col + int(delta_col / math.fabs(delta_col))

            current_point = PathPoint(next_row, next_col)
            self.pattern[current_point.row][current_point.col] = 1
            delta_row = end_point.row - current_point.row
            delta_col = end_point.col - current_point.col



    def follow_pattern(self, current, previous):
        possible_path = []
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))
        possible_path.append(PathPoint(0, 0))

        # 周围方块相对于当前点的相对位置
        offset = []
        offset.append(PathPoint(-1, -1))
        offset.append(PathPoint(-1, 0))
        offset.append(PathPoint(-1, 1))
        offset.append(PathPoint(0, -1))
        offset.append(PathPoint(0, 1))
        offset.append(PathPoint(1, -1))
        offset.append(PathPoint(1, 0))
        offset.append(PathPoint(1, 1))

        j = 0
        for i in range(0, 8, 1):
            # self.pattern 需要在 build_path_segment 中初始化
            if self.pattern[current.row + offset[i].row][current.col + offset[i].col] == 1:
                if not (((current.row + offset[i].row) == previous.row)
                         and ((current.col + offset[i].col) == previous.col)):
                    possible_path[j].row = current.row + offset[i].row
                    possible_path[j].col = current.col + offset[i].col
                    j += 1
        if j > 0:
            i = random.randint(0 , j-1)
        else:
            i = 0
        # 如果我们记录下当前走过的所有路径，那么可以直接从记录下来的路径中查找 previous
        previous.row = current.row
        previous.col = current.col
        return possible_path[i]

# 准备一些数据
entity_list = []

entity = AiEntity(30, 30)
entity.initialize_path_array()
entity.build_path_segment(PathPoint(2, 2), PathPoint(2, 10))
entity.build_path_segment(PathPoint(2, 10), PathPoint(10, 10))
entity.build_path_segment(PathPoint(10, 10), PathPoint(10, 2))
entity.build_path_segment(PathPoint(10, 2), PathPoint(2, 2))

entity_list.append(entity)

# 起始的点
start_point = PathPoint(2, 2)

import pygame
from pygame.locals import *
import time

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


class Ball(object):
    def __init__(self, row=0, col=0, color=white):
        self.row = row
        self.col = col
        self.color = color
        self.radius = square_width / 2

    def update(self, move=(0,0)):
        self.current_row_index += move[0]
        self.current_col_index += move[1]

        self.current_row_index = self.current_row_index%row
        self.current_col_index = self.current_col_index%col

        self.y = self.current_row_index * square_width + square_width / 2
        self.x = self.current_col_index * square_width + square_width / 2


def draw_ball(screen, ball):
    #print '绘制小球'
    # 绘制一个圆形
    y = ball.row * square_width + square_width / 2
    x = ball.col * square_width + square_width / 2

    position = x, y
    radius = square_width / 2
    width = 1
    color = ball.color

    # pygame.draw.circle
    # 原型：pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    # 当不传入width参数的时候，绘制的是一个填充了的圆
    pygame.draw.circle(screen, color, position, radius)


# 定义一个小球
# 小球的初始位置为运动的初始位置
ball = Ball(start_point.row, start_point.col)

# 上一秒的秒数
last_second = time.time()
# 走过的路径
record_path = []

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # 绘制黑色背景色
    screen.fill(deep_sky_blue)
    # 绘制白色方格线
    for r in range(0 , row + 1):
        pygame.draw.aaline(screen, black, (0, r * square_width), (col * square_width, r * square_width))

    for c in range(0, col + 1):
        pygame.draw.aaline(screen, black, (c * square_width, 0), (c * square_width, col * square_width))



    # 每隔0.5秒移动一次
    # 单位是秒
    current_second = time.time()
    # 每隔0.5秒移动一次
    if current_second - last_second >= 0.5:
        current = PathPoint(start_point.row, start_point.col)
        if len(record_path) >= 1:
            current.row = record_path[-1].row
            current.col = record_path[-1].col

        previous = PathPoint(start_point.row, start_point.col)
        if len(record_path) >= 2:
            previous.row = record_path[-2].row
            previous.col = record_path[-2].col

        # 移动模式
        move_pattern = entity_list[0]
        next_point = move_pattern.follow_pattern(current, previous)
        ball.row = next_point.row
        ball.col = next_point.col
        #print ball.row, ',', ball.col
        record_path.append(PathPoint(ball.row, ball.col))

        # 将当前毫秒数赋值给上一秒毫秒数
        last_second = current_second

    # 绘制两个小球
    draw_ball(screen, ball)

    pygame.display.update()

