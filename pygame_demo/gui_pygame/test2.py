#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import wx
from wx import *
import pygame
import sys

class wxSDLWindow(wx.Frame):
    def __init__(self, parent, id, title='SDL window', **options):
        options['style'] = wx.DEFAULT_FRAME_STYLE | wx.TRANSPARENT_WINDOW
        wx.Frame.__init__(*(self, parent, id, title), **options)

        self._initialized = 0
        self._resized = 0
        self._surface = None
        self.__needsDrawing = 1

        wx.EVT_IDLE(self, self.OnIdle)


    def OnIdle(self, ev):
        if not self._initialized or self._resized:
            if not self._initialized:
                # get the handle
                hwnd = self.GetHandle()

                os.environ['SDL_WINDOWID'] = str(hwnd)
                if sys.platform == 'win32':
                    os.environ['SDL_VIDEODRIVER'] = 'windib'

                pygame.init()

                wx.EVT_SIZE(self, self.OnSize)
                self._initialized = 1
        else:
            self._resized = 0

        x, y = self.GetSizeTuple()
        self._surface = pygame.display.set_mode((x, y))

        if self.__needsDrawing:
            self.draw()

    def OnPaint(self, ev):
        self.__needsDrawing = 1

    def OnSize(self, ev):
        self._resized = 1
        ev.Skip()

    def draw(self):
        raise NotImplementedError('please define a .draw() method!')

    def getSurface(self):
        return self._surface


if __name__ == "__main__":

    class CircleWindow(wxSDLWindow):
        "draw a circle in a wxPython / PyGame window"

        def draw(self):
            surface = self.getSurface()
            if surface is not None:
                topcolor = 5
                bottomcolor = 100

                pygame.draw.circle(surface, (250, 0, 0), (100, 100), 50)

                pygame.display.flip()


    def pygametest():
        app = wx.App()
        sizeT = (640, 480)
        w = CircleWindow(None, -1, size=sizeT)
        w.Show(1)
        app.MainLoop()


    pygametest()