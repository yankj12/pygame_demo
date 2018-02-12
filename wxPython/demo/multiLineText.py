#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os


# 多行文本编辑器
class my_frame(wx.Frame):

    """We simple derive a new class of frame"""
    def __init__(self, parent, title):
        self.filename = None
        self.dirname = None
        self.address = None
        width = 800
        height = width * 2 / 3

        self.count = 5

        wx.Frame.__init__(self, parent, title=title, size=(width, height))
        # 继承来自wx.Frame的__init__方法。声明一个wx.TextCtrl控件
        # （简单的文本编辑控件）
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)
        # 创建窗口底部的状态栏
        self.CreateStatusBar()
        filemenu = wx.Menu()
        menu_new = filemenu.Append(wx.ID_NEW, "New", "New a file.")
        menu_open = filemenu.Append(wx.ID_OPEN, "Open", "Open a file.")
        menu_save = filemenu.Append(wx.ID_SAVE, "Save", "Save this file.")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT, "Exit", "Exit the program.")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, u"File")

        helpmenu = wx.Menu()
        menu_about = helpmenu.Append(wx.ID_ABOUT, "About", "Information about this program.")
        menubar.Append(helpmenu, u"Help")

        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        tool_undo = self.toolbar.AddTool(wx.ID_UNDO, '', wx.Bitmap("icon/back_16.png"))
        tool_redo = self.toolbar.AddTool(wx.ID_REDO, '', wx.Bitmap("icon/more_16.png"))
        self.toolbar.EnableTool(wx.ID_REDO, False)
        self.toolbar.AddSeparator()

        tool_exit = self.toolbar.AddTool(wx.ID_EXIT, '', wx.Bitmap("icon/close_16.png"))
        self.toolbar.Realize()

        self.Centre()
        self.Show(True)

        # 把出现的事件，同需要处理的函数连接起来
        self.Bind(wx.EVT_MENU, self.on_new, menu_new)
        self.Bind(wx.EVT_MENU, self.on_open, menu_open)
        self.Bind(wx.EVT_MENU, self.on_save, menu_save)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)

        self.Bind(wx.EVT_TOOL, self.on_exit, tool_exit)
        self.Bind(wx.EVT_TOOL, self.on_undo, tool_undo)
        self.Bind(wx.EVT_TOOL, self.on_redo, tool_redo)


    def on_about(self, e):
        # 创建一个对话框，有一个ok选项
        dlg = wx.MessageDialog(self, "A small text editor.", "About small editor.", wx.OK)
        # 显示对话框
        dlg.ShowModal()
        # 完成后销毁
        dlg.Destroy()

    def on_exit(self, e):
        self.Close(True)

    def on_new(self, e):
        # 清空编辑区内容
        self.control.Clear()
        # 文件相关的属性赋值为空
        # 不清空self.dirname 默认保存到这个文件夹内
        self.filename = None
        self.address = None


    def on_open(self, e):
        """open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file.", self.dirname, "", "*.*")
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.address = os.path.join(self.dirname, self.filename)
            f = open(self.address, "r")
            file = (f.read()).decode(encoding="UTF-8")
            f.close()
            self.control.Clear()
            self.control.AppendText(file)
        dlg.Destroy()

    def on_save(self, e):
        data = (self.control.GetValue()).encode(encoding="UTF-8")
        # 保存文件
        # 新增文件进行保存的时候，需要选择保存到哪个文件夹，以及文件名是什么
        if self.address is None or self.address == "":
            # 新增
            file_dlg = wx.FileDialog(self, "Choose a file.", "", "", "*.*")
            if file_dlg.ShowModal() == wx.ID_OK:
                self.filename = file_dlg.GetFilename()
                self.dirname = file_dlg.GetDirectory()
                self.address = os.path.join(self.dirname, self.filename)
            file_dlg.Destroy()

        # 修改文件进行保存的时候，直接保存到原有文件即可
        f = open(self.address, "w")
        f.write(data)
        f.close()
        dlg = wx.MessageDialog(self, "File saved.", "Info", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        self.control.Clear()
        self.control.AppendText("Welcome to use editor.\nA small text editor.")
        self.address = None

    def on_undo(self,e):
        if self.count > 1 and self.count <= 5:
            self.count = self.count -1
        if self.count == 1:
            self.toolbar.EnableTool(wx.ID_UNDO,False)
        if self.count == 4:
            self.toolbar.EnableTool(wx.ID_REDO,True)

    def on_redo(self,e):
        if self.count < 5 and self.count >= 1:
            self.count = self.count + 1
        if self.count == 5:
            self.toolbar.EnableTool(wx.ID_REDO,False)
        if self.count == 2:
            self.toolbar.EnableTool(wx.ID_UNDO,True)

app = wx.App(False)
frame = my_frame(None, "Small Editor")
app.MainLoop()