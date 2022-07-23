import shutil

from PySide6.QtWidgets import *
from 自动更新模块 import *
import version


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(400, 600)
        self.setWindowTitle("自动更新的程序演示")
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

    def 检查更新回到回调函数(self, 数据):
        # print("数据", 数据)
        print("版本号", 数据['版本号'])
        # print("下载地址列表", 数据['下载地址列表'])
        print("mac下载地址", 数据['mac下载地址'])
        print("windows下载地址", 数据['win下载地址'])
        self.编辑框2.setHtml(数据['更新内容'])

    def 按钮2点击(self):
        print('查询最新版本')
        self.检查更新线程 = 检查更新线程(self, self.检查更新回到回调函数)
        self.检查更新线程.start()

    def closeEvent(self, event):
        event.accept()

    def 下载并更新2(self, 下载地址, 压缩包路径, 应用名称):
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

    def 检查更新回调1(self, 数据):
        # print("数据", 数据)
        print("版本号", 数据['版本号'])
        print("mac下载地址", 数据['mac下载地址'])
        print("windows下载地址", 数据['win下载地址'])
        if self.版本号 == 数据['版本号']:
            return
            # 消息框询问是否更新
        确认 = QMessageBox.question(self, "更新提示", f"发现新版本{数据['版本号']}，是否更新？")
        if 确认 == QMessageBox.Yes:
            if 系统_是否为mac系统():
                self.下载并更新2(数据['mac下载地址'], self.压缩包路径, self.应用名称)
            if 系统_是否为window系统():
                if 数据.get("windows下载地址","") == "":
                    # 提示没有找到windows下载地址
                    QMessageBox.warning(self, "提示", "没有找到windows下载地址")
                    return
                self.下载并更新2(数据['windows下载地址'], self.压缩包路径, self.应用名称)

    def 按钮点击(self):
        # EXE文件路径 = r"C:\Users\csuil\.virtualenvs\QtEsayDesigner\Scripts\dist\my_app1.0.exe"
        # 更新自己Window应用(EXE文件路径)
        print('查询最新版本')
        # 获取系统下载文件夹路径
        self.应用名称 = "my_app.app"
        下载文件夹路径 = os.path.expanduser('~/Downloads')
        self.压缩包路径 = os.path.abspath(下载文件夹路径 + f"/{self.应用名称}.zip")
        print("self.压缩包路径", self.压缩包路径)
        self.检查更新线程 = 检查更新线程(self, self.检查更新回调1)
        self.检查更新线程.start()



if __name__ == '__main__':
    # 获取命令行参数
    传入参数 = sys.argv
    # print("传入参数", 传入参数)
    if len(传入参数) == 2:
        参数1 = 传入参数[1]
        if 参数1 == "test":
            print("app run success")
            # 停止脚本
            sys.exit(0)

    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec())
