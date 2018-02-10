#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

# 多行文本编辑器
class my_frame(wx.Frame):

    """We simple derive a new class of frame"""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300, 200))
        # 继承来自wx.Frame的__init__方法。声明一个wx.TextCtrl控件
        # （简单的文本编辑控件）
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)
        # 创建窗口底部的状态栏
        self.CreateStatusBar()
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_EXIT, "Exit", "Exit the program.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, "About", "Information about this program.")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, u"设置")
        self.SetMenuBar(menubar)
        self.Show(True)


app = wx.App(False)
frame = my_frame(None, "Small Editor")
app.MainLoop()