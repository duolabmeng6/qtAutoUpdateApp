import json
import sys

from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout, QApplication, QMainWindow, QPushButton

import version
import 自动更新模块

全局_项目名称 = "duolabmeng6/qtAutoUpdateApp"
全局_应用名称 = "my_app.app"
全局_当前版本 = version.version
全局_官方网址 = "https://github.com/duolabmeng6/qtAutoUpdateApp"


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.init_ui()

    def 按钮_检查更新点击(self):
        # 弹出窗口
        self.winUpdate = 自动更新模块.窗口_更新软件(Github项目名称=全局_项目名称,
                                        应用名称=全局_应用名称,
                                        当前版本号=全局_当前版本,
                                        官方网址=全局_官方网址)
        self.winUpdate.show()

    def init_ui(self):
        self.resize(400, 300)
        self.setWindowTitle(f"自动更新的程序演示")
        self.show()
        # 创建容器
        self.main_widget = QWidget()

        self.按钮_检查更新 = QPushButton(self.main_widget)
        self.按钮_检查更新.clicked.connect(self.按钮_检查更新点击)
        self.按钮_检查更新.resize(160, 100)
        self.按钮_检查更新.setText(f'检查更新')
        self.按钮_检查更新.show()

        self.label = QLabel(self.main_widget)
        self.label.setText(f'当前版本:{全局_当前版本}')
        self.label.resize(160, 100)
        self.label.show()

        self.label2 = QLabel(self.main_widget)
        self.label2.setText(f'最新版本:查询中')
        self.label2.resize(160, 100)
        self.label2.show()

        # 编辑框
        self.textEdit = QTextEdit(self.main_widget)
        self.textEdit.resize(400, 150)
        self.textEdit.show()

        # 创建布局容器并应用
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.按钮_检查更新)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.textEdit, 1)
        self.setCentralWidget(self.main_widget)

        self.检查更新线程 = 自动更新模块.检查更新线程(全局_项目名称, self.检查更新回到回调函数)
        self.检查更新线程.start()

    def 检查更新回到回调函数(self, 数据):
        print("数据", 数据)
        最新版本 = 数据['版本号']
        self.label2.setText(f'最新版本:{最新版本}')
        self.textEdit.setText(json.dumps(数据, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    自动更新模块.初始化()

    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec())
