# -*- coding: utf-8 -*-
import os


def 查看系统所有环境变量():
    from icecream import ic
    # 打印系统所有的环境变量
    for item in os.environ:
        name = item
        value = os.environ[item]
        ic(name, value)
查看系统所有环境变量()

tagName = os.environ.get('GITHUB_REF_NAME')
print("tagName:", tagName)
# 获取运行目录
print("run dir:", os.getcwd())
# 获取文件目录
文件目录 = os.path.dirname(__file__)
print("file dir:", os.path.dirname(__file__))
# 覆盖写出文件 version.py 中
with open(f'{文件目录}/version.py', 'w') as f:
    f.write(f'version = "{tagName}"')

exit()
