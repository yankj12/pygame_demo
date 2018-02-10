#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx

# 创造一个wx.App实例。参数是“False”的意思是不将stdout和stderr重定向到一个窗口，这个参数是“True”对这个例子没有影响。
app = wx.App(False)
# 创建一个顶级窗口，语法为wx.Frame（parent，ID，标题）。这个例子中wx.ID_ANY wxWidgets为我们挑选一个id
frame = wx.Frame(None, wx.ID_ANY, "Hello world")
# 显示窗口
frame.Show()
# 主循环，处理事件
app.MainLoop()