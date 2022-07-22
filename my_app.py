import json
import os
import sys
import threading

from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from 压缩包文件处理 import *
from 文件下载模块 import *
from 自动更新模块 import *
import version
from 自动更新读取版本模块 import 获取最新版本号和下载地址


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(400, 600)
        self.setWindowTitle("自动更新测试组件学习")
        self.show()
        self.版本号 = version.version

        # 创建按钮 测试更新
        self.按钮 = QPushButton(self)
        self.按钮.clicked.connect(self.按钮点击)
        self.按钮.move(100, 100)
        self.按钮.resize(160, 100)

        self.按钮.setText(f'检查更新 当前版本 {version.version}')
        self.按钮.show()
        # 编辑一个纯文本框
        self.编辑框 = QTextEdit(self)
        self.编辑框.move(0, 200)
        self.编辑框.resize(400, 200)
        self.编辑框.setText('日志')
        self.编辑框.show()

        self.编辑框2 = QTextEdit(self)
        self.编辑框2.move(0, 400)
        self.编辑框2.resize(400, 200)
        self.编辑框2.setText('显示更新信息')
        self.编辑框2.show()

        # 创建进度条
        self.进度条 = QProgressBar(self)
        self.进度条.move(0, 0)
        self.进度条.resize(300, 20)
        # 设置高度为60

        self.进度条.setOrientation(QtCore.Qt.Horizontal)
        self.进度条.setRange(0, 100)
        self.进度条.setValue(0)
        # self.进度条.setFormat("％p％")
        self.进度条.show()
        # 创建按钮 查询最新版
        self.按钮2 = QPushButton(self)
        self.按钮2.clicked.connect(self.按钮2点击)
        self.按钮2.move(100, 0)
        self.按钮2.resize(160, 100)
        self.按钮2.setText(f'查询最新版')
        self.按钮2.show()

        # 启动qt的线程

    def 按钮2点击(self):
        print('查询最新版本')

        def 回调函数(数据):
            # print("数据", 数据)
            print("版本号", 数据['版本号'])
            # print("下载地址列表", 数据['下载地址列表'])
            print("mac下载地址", 数据['mac下载地址'])
            print("windows下载地址", 数据['win下载地址'])
            self.编辑框2.setHtml(数据['更新内容'])

        self.检查更新线程 = 检查更新线程(self, 回调函数)
        self.检查更新线程.start()

    def closeEvent(self, event):
        event.accept()

    def 按钮点击(self):
        print('查询最新版本')
        # 获取系统下载文件夹路径
        应用名称 = "my_app.app"
        下载文件夹路径 = os.path.expanduser('~/Downloads')
        压缩包路径 = os.path.abspath(下载文件夹路径 + f"/{应用名称}.zip")
        print("压缩包路径", 压缩包路径)

        def 下载并更新2(下载地址):
            print(f"压缩包路径{压缩包路径}")
            self.下载文件线程 = 下载文件线程类(
                下载地址=下载地址,
                保存地址=压缩包路径,
                窗口=self,
                编辑框=self.编辑框,
                进度条=self.进度条,
                应用名称=应用名称
            )
            self.下载文件线程.start()

        def 检查更新回调1(数据):
            # print("数据", 数据)
            print("版本号", 数据['版本号'])
            print("mac下载地址", 数据['mac下载地址'])
            print("windows下载地址", 数据['win下载地址'])

            if self.版本号 == 数据['版本号']:
                return
                # 消息框询问是否更新

            确认 = QMessageBox.question(self, "更新提示", f"发现新版本{数据['版本号']}，是否更新？")
            if 确认 == QMessageBox.Yes:
                下载并更新2(数据['mac下载地址'])

        self.检查更新线程 = 检查更新线程(self, 检查更新回调1)
        self.检查更新线程.start()


app = QApplication([])
win = Main()
sys.exit(app.exec())
