#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 记住上面这行是必须的，而且保存文件的编码要一致！

import pygame
from pygame.locals import *
from sys import exit
import threading
from time import ctime,sleep


pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

# font = pygame.font.SysFont("宋体", 40)
# 上句在Linux可行，在我的Windows 7 64bit上不行，XP不知道行不行
# font = pygame.font.SysFont("simsunnsimsun", 40)
# 用get_fonts()查看后看到了这个字体名，在我的机器上可以正常显示了
# font = pygame.font.Font("simsun.ttc", 40) # 如果要使用这句，需要添加一个simsun.ttc的字体
font = pygame.font.SysFont("simsunnsimsun", 10)
# 这句话总是可以的，所以还是TTF文件保险啊
text_surface = font.render(u"你好", True, (0, 0, 255))

x = 0
y = (480 - text_surface.get_height()) / 4

background = pygame.image.load("sushiplate.jpg").convert()
screen.blit(background, (0, 0))


class MyThread(threading.Thread):
    x, y

    def __init__(self,threadName, x, y):
        threading.Thread.__init__(self,name=threadName)
        self.x = x
        self.y = y


    def run(self):
        x = self.x
        y = self.y

        while True:
            y = y - 0.5
            self.x = x
            self.y = y

            if y <= 0:
                print u'文字消息即将退出窗体'
                break
            else:
                sleep(0.1)

t = MyThread(u't1', x, y)
t.setDaemon(True)
t.start()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.blit(background, (0, 0))
    x = t.x
    y = t.y
    if y > 0:
        screen.blit(text_surface, (x, y))
    pygame.display.update()