import json
import requests
import time
from pdlearn import color


def get_native_json():
    with open("./pdlearn/version_info.json", encoding="utf-8") as v:
        content = v.read()
        return json.loads(content)


def up_info():
    print(color.yellow("[*] 正在联网获取更新信息...(更新显示不会打断之前输入等操作)"))

    __INFO = "TechXueXi最新下载地址为 https://github.com/TechXueXi/TechXueXi"
    __SITE = "科技强国官方网站：https://techxuexi.js.org"

    # vercel_url = "https://techxuexi.vercel.app/Update.html"
    jsdelivery_url = "https://cdn.jsdelivr.net/gh/TechXueXi/TechXueXi@master/SourcePackages/pdlearn/version_info.json"
    try:
        native_info = get_native_json()
        remote_json = requests.get(jsdelivery_url).content.decode("utf8")
        remote_info = json.loads(remote_json)
        print(remote_info["notice"])
    except:
        print(color.yellow("[*] 版本信息网络错误"))
    try:
        remote_least_version=int((str(remote_info["least_version"]))[1:])
        int_native_version = int((str(native_info["techxuexi_version"]))[1:])
        if int_native_version < remote_least_version:
            old_version_warning=remote_info["old_version_warning"]
            print(color.yellow("[*] 您的版本太低，程序不会继续运行。请升级："))
            print(old_version_warning)
            while True:
                time.sleep(6000)
    except:
        print(color.yellow("[*] 查询本版本是否能继续使用，错误"))
    try:
        native_version = native_info["techxuexi_version"]
        native_update_logs = native_info["techxuexi_update_log"]
        
        remote_version = remote_info["techxuexi_version"]
        remote_update_logs = remote_info["techxuexi_update_log"]
        print(color.yellow("[*] " + __INFO))
        print(color.yellow("[*] 程序版本为：{}".format(native_version)))
        print(color.yellow("[*] 最新稳定版为：{}".format(remote_version)))
        if remote_version > native_version:  # 有新版本
            print(color.red("[*] 当前不是最新版本，建议更新"))
            print(color.red("[*] " + "=" * 60))
            print(color.red("[*] 更新提要："))
            for log in remote_update_logs:
                if log["version"] > native_version:
                    print(color.red("[*] " + log["version"]))
                    print(color.red(log["info"]))
                else:
                    print(color.yellow("[*] " + __INFO))
                    print(color.yellow("[*] " + __SITE))
                    break
    except:
        print(color.yellow("[*] 版本信息网络错误"))


if __name__ == '__main__':
    up_info()
