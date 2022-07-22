import os
import sys
import threading

from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from 压缩包文件处理 import *
from 文件下载模块 import *
from 自动更新模块 import *


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(400, 400)
        self.setWindowTitle("自动更新测试组件学习")
        self.show()
        # 创建按钮 测试更新
        self.按钮 = QPushButton(self)
        self.按钮.clicked.connect(self.按钮点击)
        self.按钮.move(100, 100)
        self.按钮.resize(160, 100)
        self.按钮.setText('测试更新 当前版本 1.0')
        self.按钮.show()
        # 编辑一个纯文本框
        self.编辑框 = QTextEdit(self)
        self.编辑框.move(0, 200)
        self.编辑框.resize(400, 200)
        self.编辑框.setText('编辑框')
        self.编辑框.show()
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

    def closeEvent(self, event):
        event.accept()

    def 按钮点击(self):
        压缩包路径 = os.path.abspath("./dist/QtEsayDesigner_MacOS.zip")
        print(f"压缩包路径{压缩包路径}")
        self.下载文件线程 = 下载文件线程类(
            下载地址="https://github.com/duolabmeng6/QtEsayDesigner/releases/download/0.0.32/QtEsayDesigner_MacOS.zip",
            保存地址=压缩包路径,
            窗口=self,
            编辑框=self.编辑框,
            进度条=self.进度条
        )
        self.下载文件线程.start()

        # return ""
        # 更新状态, app路径 = 更新自己MacOS应用(
        #     "/Users/chensuilong/Desktop/pythonproject/autotest/dist/my_app.2.0.zip",
        #     "my_app.app"
        # )
        # if 更新状态:
        #     QMessageBox.information(self, "提示", "更新成功")
        #     self.close()
        #     os.system("open -n -a " + app路径)
        # else:
        #     QMessageBox.information(self, "提示", "更新失败")


app = QApplication([])
win = Main()
sys.exit(app.exec())
