#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx

app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, "Hello world")
frame.Show()
app.MainLoop()