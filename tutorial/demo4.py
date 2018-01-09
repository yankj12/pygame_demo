#!/usr/bin/env python
# -*- coding:utf-8 -*-


my_name = u"你好"
import pygame
pygame.init()
my_font = pygame.font.SysFont("simsunnsimsun", 64)
name_surface = my_font.render(my_name, True, (0, 0, 0), (255, 255, 255))
pygame.image.save(name_surface, "name.png")


