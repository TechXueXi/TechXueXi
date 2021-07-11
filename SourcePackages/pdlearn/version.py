import json
import requests
from pdlearn import color


def get_native_version():
    with open("./pdlearn/version_info.json", encoding="utf-8") as v:
        content = v.read()
        return json.loads(content)["techxuexi_version"]


def up_info():
    print(color.yellow("[*] 正在联网获取更新信息...(更新显示不会打断之前输入等操作)"))

    __INFO = "TechXueXi最新下载地址为 https://github.com/TechXueXi/TechXueXi"
    __SITE = "科技强国官方网站：https://techxuexi.js.org"

    # vercel_url = "https://techxuexi.vercel.app/Update.html"
    jsdelivery_url = "https://cdn.jsdelivr.net/gh/TechXueXi/TechXueXi@dev/SourcePackages/pdlearn/version_info.json"
    try:
        native_version = get_native_version()
        remote_json = requests.get(jsdelivery_url).content.decode("utf8")
        remote_info = json.loads(remote_json)
        remote_version = remote_info["techxuexi_version"]
        remote_update_logs = remote_info["techxuexi_update_log"]
        print(color.yellow("[*] " + __INFO))
        print(color.yellow("[*] 程序版本为：{}".format(native_version)))
        print(color.yellow("[*] 最新版本为：{}".format(remote_version)))
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
