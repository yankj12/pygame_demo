#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *

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


while True:
    if pygame.event.poll().type == QUIT: break

    # 绘制黑色背景色
    screen.fill(deep_sky_blue)
    # 绘制白色方格线
    for r in range(0 , row + 1):
        pygame.draw.aaline(screen, black, (0, r * square_width), (col * square_width, r * square_width))

    for c in range(0, col + 1):
        pygame.draw.aaline(screen, black, (c * square_width, 0), (c * square_width, col * square_width))

    pygame.display.update()