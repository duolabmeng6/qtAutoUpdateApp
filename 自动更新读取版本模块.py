# https://github.com/duolabmeng6/qtAutoUpdateApp/releases
# 读取github项目中的最新的版本号

from github import Github


# using an access token


def 获取最新版本号和下载地址(project_name):
    g = Github("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")
    repo = g.get_repo(project_name)
    latest_release = repo.get_latest_release()
    版本号 = latest_release.tag_name
    body = latest_release.body
    created_at = latest_release.created_at

    mac下载地址 = ""
    win下载地址 = ""
    下载地址列表 = []
    for item in latest_release.get_assets():
        下载地址 = item.browser_download_url
        文件名 = item.name
        下载地址列表.append([
            文件名, 下载地址
        ])
        if 文件名.find('MacOS.zip') != -1:
            mac下载地址 = 下载地址
        if 文件名.find('.exe') != -1:
            win下载地址 = 下载地址

    return {
        "版本号": 版本号,
        "下载地址列表": 下载地址列表,
        "mac下载地址": mac下载地址,
        "win下载地址": win下载地址,
        "更新内容": body,
        "发布时间": str(created_at)
    }


# 测试
if __name__ == '__main__':
    data = 获取最新版本号和下载地址("duolabmeng6/qtAutoUpdateApp")
    print(data)
