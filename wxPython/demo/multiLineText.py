#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os


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
        menu_open = filemenu.Append(wx.ID_OPEN, "Open", "Open a file.")
        menu_exit = filemenu.Append(wx.ID_EXIT, "Exit", "Exit the program.")
        filemenu.AppendSeparator()
        menu_about = filemenu.Append(wx.ID_ABOUT, "About", "Information about this program.")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, u"设置")
        self.SetMenuBar(menubar)
        self.Show(True)

        # 把出现的事件，同需要处理的函数连接起来
        self.Bind(wx.EVT_MENU, self.on_open, menu_open)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)


    def on_about(self, e):
        # 创建一个对话框，有一个ok选项
        dlg = wx.MessageDialog(self, "A small text editor.", "About small editor.", wx.OK)
        # 显示对话框
        dlg.ShowModal()
        # 完成后销毁
        dlg.Destroy()

    def on_exit(self, e):
        self.Close(True)

    def on_open(self, e):
        """open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file.", self.dirname, "", "*.*")
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), "r")
        dlg.Destroy()


app = wx.App(False)
frame = my_frame(None, "Small Editor")
app.MainLoop()