#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

# 多行文本编辑器
class my_frame(wx.Frame):

    """We simple derive a new class of frame"""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300, 100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)


app = wx.App(False)
frame = my_frame(None, "Small Editor")
app.MainLoop()