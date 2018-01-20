#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *


class Brush():
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 1
        self.drawing = False

    def start_draw(self):
        self.drawing = True

    def end_draw(self):
        self.drawing = False

    def draw(self, pos):
        if self.drawing:
            pygame.draw.circle(self.screen, self.color, pos, self.size)


class Painter():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)

    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            # max fps limit
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    pass
                elif event.type == MOUSEBUTTONDOWN:
                    pass
                elif event.type == MOUSEMOTION:
                    pass
                elif event.type == MOUSEBUTTONUP:
                    pass
                elif event.type == KEYDOWN:
                    # press esc to clear screen
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    self.brush.start_draw()
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()

            pygame.display.update()


if __name__ == '__main__':
    app = Painter()
    app.run()