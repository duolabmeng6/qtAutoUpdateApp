import json
import os
import sys

from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from 压缩包文件处理 import zip解压2
from 文件下载模块 import 下载文件
from 自动更新读取版本模块 import 获取最新版本号和下载地址


def 取自身MacOs应用路径():
    # 如果不处于编译状态反馈空
    try:
        编译后路径 = sys._MEIPASS
    except Exception:
        编译后路径 = os.path.abspath(".")
        # 调试的
        # 编译后路径 = "/Users/chensuilong/Desktop/pythonproject/autotest/dist/my_app.app/Contents/MacOS"
    app目录 = 编译后路径[:编译后路径.rfind('/')]
    app目录 = app目录[:app目录.rfind('/')]
    父目录名称 = 编译后路径[编译后路径.rfind('/') + 1:]
    if 父目录名称 == "MacOS":
        return app目录
    else:
        return ""


def 更新自己MacOS应用(资源压缩包, 应用名称="my_app.app"):
    # 资源压缩包 = "/Users/chensuilong/Desktop/pythonproject/autotest/dist/my_app.2.0.zip"
    # 应用名称 例如 my_app.app 这你的压缩包里面压缩的应用文件夹名称
    MacOs应用路径 = 取自身MacOs应用路径()
    if MacOs应用路径 != "":
        app目录父目录 = MacOs应用路径[:MacOs应用路径.rfind('/')]
        print(f"资源压缩包 {资源压缩包} app目录父目录{app目录父目录} MacOs应用路径{MacOs应用路径}")
        if MacOs应用路径 != "":
            zip解压2(资源压缩包, app目录父目录, [应用名称 + '/Contents/'])
            MacOs应用路径 = os.path.join(app目录父目录 + 应用名称)
            return True, MacOs应用路径
    else:
        print("非MacOS编译环境")
        return False, ""


class 下载文件线程类(QThread):
    刷新界面事件 = QtCore.Signal(int, str)  # 进度 提示文本
    任务完成事件 = QtCore.Signal(bool, str)  # 下载结果 保存路径

    def __init__(self, *args, **kwargs):
        super(下载文件线程类, self).__init__()
        self.窗口 = kwargs.get('窗口')
        self.下载地址 = kwargs.get('下载地址')
        self.保存地址 = kwargs.get('保存地址')
        self.编辑框 = kwargs.get('编辑框')
        self.进度条 = kwargs.get('进度条')
        self.应用名称 = kwargs.get('应用名称')

        self.刷新界面事件.connect(self.刷新界面)
        self.任务完成事件.connect(self.任务完成)

    def run(self):
        if self.下载地址 == None:
            print("请传入下载地址")
            return

        def 进度(进度百分比, 已下载大小, 文件大小, 下载速率, 剩余时间):
            信息 = f"进度 {进度百分比}% 已下载 {已下载大小}MB 文件大小 {文件大小}MB 下载速率 {下载速率}MB 剩余时间 {剩余时间}秒"
            self.刷新界面事件.emit(进度百分比, 信息)

        try:
            下载结果 = 下载文件(self.下载地址, self.保存地址, 进度)
            self.任务完成事件.emit(True, self.保存地址)
        except:
            self.任务完成事件.emit(False, self.保存地址)

    def 刷新界面(self, 进度, 信息):
        if self.编辑框:
            self.编辑框.setText(str(信息))
        if self.进度条:
            self.进度条.setValue(int(进度))

    def 任务完成(self, 下载结果, 保存地址):
        print("下载结果", 下载结果)
        print("保存地址", 保存地址)
        self.编辑框.setText(f"下载完成 {保存地址}")
        # 取绝对路径
        更新状态, app路径 = 更新自己MacOS应用(
            资源压缩包=保存地址,
            应用名称=self.应用名称
        )
        if 更新状态:
            QMessageBox.information(self.窗口, "提示", "更新成功")
            self.窗口.close()
            运行命令 = "open -n -a " + app路径
            QMessageBox.information(self.窗口, "提示", 运行命令)
            os.system(运行命令)
        else:
            QMessageBox.information(self.窗口, "提示", "更新失败")


class 检查更新线程(QThread):
    def __init__(self, 窗口, 回调函数):
        super(检查更新线程, self).__init__()
        self.编辑框 = 窗口.编辑框
        # 绑定线程开始事件
        self.started.connect(self.ui_开始)
        # 绑定线程结束事件
        self.finished.connect(self.ui_结束)
        self.回调函数 = 回调函数

    def run(self):
        data = 获取最新版本号和下载地址("duolabmeng6/qtAutoUpdateApp")
        self.数据 = data

    def ui_开始(self):
        self.编辑框.setText(f'查询最新版本')

    def ui_结束(self):
        data = json.dumps(self.数据, indent=4, ensure_ascii=False)
        self.编辑框.setText(data)
        self.回调函数(self.数据)
