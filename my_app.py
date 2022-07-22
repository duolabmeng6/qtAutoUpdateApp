import os
import sys
import threading

from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from 压缩包文件处理 import *
from 文件下载模块 import *


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
        # self.窗口 = kwargs.get('窗口')
        self.下载地址 = kwargs.get('下载地址')
        self.保存地址 = kwargs.get('保存地址')
        self.编辑框 = kwargs.get('编辑框')
        self.进度条 = kwargs.get('进度条')

        self.刷新界面事件.connect(self.刷新界面)

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

        self.timer = QTimer(self)  # 3
        self.timer.timeout.connect(self.更新线程)

    进度值 = 0

    def 更新线程(self):
        # for 进度 in range(100):
        self.进度值 = self.进度值 + 1
        self.进度条.setValue(self.进度值)
        if self.进度值 < 100:
            # QtCore.QTimer.singleShot(50, lambda: self.更新线程())
            pass
        else:
            self.进度值 = 0
            self.timer.stop()

    def closeEvent(self, event):
        # 关闭窗口时 停止线程
        # self.下载文件线程.terminate()
        # self.下载文件线程.wait()
        event.accept()

    def 任务完成(self, 下载结果, 保存地址):
        print("下载结果", 下载结果)
        print("保存地址", 保存地址)
        self.编辑框.setText(f"下载完成 {保存地址}")

        # 取绝对路径
        更新状态, app路径 = 更新自己MacOS应用(
            资源压缩包=保存地址,
            应用名称="QtEsayDesigner.app"
        )
        if 更新状态:
            QMessageBox.information(self, "提示", "更新成功")
            self.close()
            os.system("open -n -a " + app路径)
        else:
            QMessageBox.information(self, "提示", "更新失败")

    def 按钮点击(self):
        压缩包路径 = os.path.abspath("QtEsayDesigner_MacOS.zip")
        print(f"压缩包路径{压缩包路径}")
        self.下载文件线程 = 下载文件线程类(
            下载地址="https://github.com/duolabmeng6/QtEsayDesigner/releases/download/0.0.32/QtEsayDesigner_MacOS.zip"
            , 保存地址=压缩包路径
            , 编辑框=self.编辑框
            , 进度条=self.进度条
        )
        self.下载文件线程.任务完成事件.connect(self.任务完成)
        self.下载文件线程.start()

        return ""
        更新状态, app路径 = 更新自己MacOS应用(
            "/Users/chensuilong/Desktop/pythonproject/autotest/dist/my_app.2.0.zip",
            "my_app.app"
        )
        if 更新状态:
            QMessageBox.information(self, "提示", "更新成功")
            self.close()
            os.system("open -n -a " + app路径)
        else:
            QMessageBox.information(self, "提示", "更新失败")


app = QApplication([])
win = Main()
sys.exit(app.exec())
