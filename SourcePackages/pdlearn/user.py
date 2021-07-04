import os
import re
import time
import pickle
import base64
from sys import argv
from pdlearn import score
from pdlearn import file
from pdlearn import color

def get_userId(cookies):
    userId, total, scores = score.get_score(cookies)
    return userId

def get_fullname(userId):
    fullname = ""
    status = get_user_status()
    for i in status["userId_mapping"]:
        nickname = status["userId_mapping"][i]
        if(str(userId) == i):
            fullname = i + '_' + nickname
            break
    if(fullname == ""):
        print("查找 userId: " + str(userId) + " 失败...")
        pattern = re.compile(u'^[a-zA-Z0-9_\u4e00-\u9fa5]+$')
        while True:
            input_name = 'user1'  # input("将为此 userId 添加一个新用户。请输入此用户昵称：")
            if(pattern.search(input_name) != None):
                break
            else:
                print("输入不符合要求，输入内容只能为：英文字母、数字、下划线、中文。")
        save_fullname(str(userId) + '_' + input_name)
        return get_fullname(userId)
    return fullname

def get_nickname(userId):
    return get_fullname(userId).split('_', 1)[1]

def save_fullname(fullname):
    status = get_user_status()
    userId = fullname.split('_', 1)[0]
    nickname = fullname.split('_', 1)[1]
    status["userId_mapping"][userId] = nickname
    save_user_status(status)

def get_user_status():
    template_json_str = '''{\n    "#-说明1":"此文件是保存用户数据及登陆状态的配置文件",'''+\
                        '''\n    "#-说明2":"程序会自动读写该文件。",'''+\
                        '''\n    "#-说明3":"如不熟悉，请勿自行修改内容。错误修改可能导致程序崩溃",'''+\
                        '''\n    "#____________________________________________________________":"",'''+\
                        '''\n    "last_userId":0,\n    "userId_mapping":{\n        "0":"default"\n    }\n}'''
    status = file.get_json_data("user/user_status.json", template_json_str)
    save_user_status(status)
    # print(status)
    return status

def update_last_user(userId):
    status = get_user_status()
    status["last_userId"] = userId
    save_user_status(status)

def save_user_status(status):
    file.save_json_data("user/user_status.json", status)

def get_cookie(userId):
    userId = str(userId)
    template_json_str = '''{}'''
    cookies_json_obj = file.get_json_data("user/cookies.json", template_json_str)
    for i in cookies_json_obj:
        if(i == userId):
            cookies_b64 = cookies_json_obj[i]
            cookies_bytes = base64.b64decode(cookies_b64)
            cookie_list = pickle.loads(cookies_bytes)
            for d in cookie_list: # 检查是否过期
                if 'name' in d and 'value' in d and 'expiry' in d:
                    expiry_date = int(d['expiry'])
                    if expiry_date > (int)(time.time()):
                        pass
                    else:
                        return []
            return cookie_list
    return []

def save_cookies(cookies):
    # print(type(cookies), cookies)
    template_json_str = '''{}'''
    cookies_json_obj = file.get_json_data("user/cookies.json", template_json_str)
    userId = get_userId(cookies)
    cookies_bytes = pickle.dumps(cookies)
    cookies_b64 = base64.b64encode(cookies_bytes)
    cookies_json_obj[str(userId)] = str(cookies_b64, encoding='utf-8')
    # print(type(cookies_json_obj), cookies_json_obj)
    file.save_json_data("user/cookies.json", cookies_json_obj)

def get_article_video_json():
    template_json_str = '''{"#此文件记录用户的视频和文章的浏览进度":"","article_index":{},"video_index":{}}'''
    article_video_json = file.get_json_data("user/article_video_index.json", template_json_str)
    return article_video_json

def get_index(userId, index_type):
    article_video_json = get_article_video_json()
    indexs = article_video_json[index_type]
    if(str(userId) in indexs.keys()):
        index = indexs[str(userId)]
    else:
        index = 0
        article_video_json[index_type][str(userId)] = index
        file.save_json_data("user/article_video_index.json", article_video_json)
    return int(index)

def save_index(userId, index, index_type):
    article_video_json = get_article_video_json()
    article_video_json[index_type][str(userId)] = index
    file.save_json_data("user/article_video_index.json", article_video_json)

def get_article_index(userId):
    return get_index(userId, "article_index")

def save_article_index(userId, index):
    return save_index(userId, index, "article_index")

def get_video_index(userId):
    return get_index(userId, "video_index")

def save_video_index(userId, index):
    return save_index(userId, index, "video_index")

def get_default_userId():
    status = get_user_status()
    default_userId = status['last_userId']
    return default_userId

def get_default_nickname():
    return get_nickname(get_default_userId())

def get_default_fullname():
    return get_fullname(get_default_userId())

def check_default_user_cookie():
    default_userId = get_default_userId()
    default_fullname = get_default_fullname()
    default_nickname = get_default_nickname()
    print_list = [color.blue(str(default_userId)), color.blue(default_nickname)]
    print("=" * 60, "\n默认用户ID：{0[0]}，默认用户昵称：{0[1]}".format(print_list), end=" ")
    cookies = get_cookie(default_userId)
    if not cookies:
        print(color.red("【无有效cookie信息，需要登录】"))
        return []
    else:
        print(color.green("（cookie信息有效）"))
        return cookies


# 如有多用户，打印各个用户信息
def list_user():
    status = get_user_status()
    mapping = status['userId_mapping']
    map_count = len(mapping)
    if(map_count > 2):
        print("检测到您有多用户：", end="")
        for i in mapping:
            print(color.blue(i + "_" + mapping[i]), end="; ")
        print("(暂不支持切换用户)")

# 多用户中选择一个用户，半成品
def select_user():
    status = get_user_status()
    mapping = status['userId_mapping']
    map_keys = []
    map_values = []
    map_count = len(mapping)
    for i in mapping:
        map_keys.append(i)
        map_values.append(mapping[i])
    print("=" * 60)
    if(map_count > 2):
        print("检测到多用户：")
        for i in range(map_count):
            print(i, " ", map_keys[i], " ", map_values[i])
        No = int(input("请选择用户序号："))
        if(No < 0 or No >= map_count):
            print("输入的范围不对。")
            exit()
        else:
            userId = map_keys[No]
            fullname = get_fullname(userId)
    else:
        print("单用户。用户名：", get_default_userId(), "，昵称：", get_default_nickname())


# 仅适用于Windows的关机，有待改进
def shutdown(stime):
    if stime:
        stime = int(stime)
        os.system('shutdown -s -t {}'.format(stime))
        for i in range(stime):
            print("\r{}秒后关机".format(stime - i), end="")
            time.sleep(1)
    else:
        print("无自动关机任务，已释放程序内存，1分钟后窗口将自动关闭")
        # time.sleep(600)
        os.system("timeout 60")
