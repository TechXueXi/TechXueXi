import requests
from pdlearn import color


def up_info():
    print(color.yellow("[*] 正在联网获取更新信息...(更新显示不会打断之前输入等操作)"))

    __Version = "v20210605"

    __INFO = "TechXueXi最新下载地址为 https://github.com/TechXueXi/TechXueXi"
    try:
        update_log = requests.get(
            "https://techxuexi.vercel.app/Update.html").content.decode(
            "utf8")
        update_log = update_log.split("\n")
        print(color.yellow("[*] " + __INFO))
        print(color.yellow("[*] 程序版本为：{}".format(__Version)))
        print(color.yellow("[*] 最新版本为：{}".format(update_log[1].split("=")[1])))
        if __Version != update_log[1].split("=")[1]:
            print(color.red("[*] 当前不是最新版本，建议更新"))
            print(color.red("[*] =" * 60))
            print(color.red("[*] 更新提要："))
            for i in update_log[2:]:
                print(color.red("[*] " + i))
    except:
        print(color.yellow("[*] 版本信息网络错误"))


if __name__ == '__main__':
    up_info()
