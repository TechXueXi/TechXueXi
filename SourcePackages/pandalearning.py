import math
import os
import sys
import time
from sys import argv

from pdlearn import boot

boot.check_environment()
try:
    # 在此处导入所有 pdlearn 内的模块
    from pdlearn import globalvar as gl
    from pdlearn import color, score, threads, user, version
    from pdlearn.answer_question import daily, weekly, zhuanxiang
    from pdlearn.article_video import article, video
    from pdlearn.config import cfg_get
    from pdlearn.mydriver import Mydriver
    from pdlearn.score import show_score, show_scorePush
except ImportError as e:
    boot.try_pip_install(exception=e)


def get_argv():
    if gl.is_init != True:
        gl.init_global()
        if len(argv) > 2:
            if argv[2] == "hidden":
                gl.nohead = True
            elif argv[2] == "show":
                gl.nohead = False
        if len(argv) > 3:
            if argv[3] == "single":
                gl.lock = True
            elif argv[3] == "multithread":
                gl.lock = False
        if len(argv) > 4:
            if argv[4].isdigit():
                gl.stime = argv[4]
    return gl.nohead, gl.lock, gl.stime, gl.single


def start_learn(uid, name):
    #  0 读取版本信息
    start_time = time.time()
    nohead, lock, stime, Single = get_argv()
    print("是否无头模式：{0} {1}".format(nohead, os.getenv('Nohead')))
    cookies = user.get_cookie(uid)
    if nohead == True:
        TechXueXi_mode = "3"
    else:
        TechXueXi_mode = str(cfg_get("base.ModeType", 3))
        print("当前选择模式：" + TechXueXi_mode + "\n" + "=" * 60)

    if not name:
        user_fullname = user.get_fullname(uid)
        name = user_fullname.split('_', 1)[1]
    else:
        user_fullname = uid+"_"+name

    if not cookies or TechXueXi_mode == "0":
        msg = ""
        if name == "新用户":
            msg = "需要增加新用户，请扫码登录，否则请无视"
        else:
            msg = name+" 登录信息失效，请重新扫码"
        # print(msg)
        gl.pushprint(msg, chat_id=uid)
        if gl.pushmode == "6":
            gl.pushprint("web模式跳过自动获取二维码,请手动点击添加按钮", chat_id=uid)
            print(color.red("【#️⃣】 若直接退出请运行：webserverListener.py"))
            return
        driver_login = Mydriver()
        cookies = driver_login.login()
        driver_login.quit()
        if not cookies:
            print("登录超时")
            return
        user.save_cookies(cookies)
        uid = user.get_userId(cookies)
        user_fullname = user.get_fullname(uid)
        name = user_fullname.split('_', 1)[1]
        user.update_last_user(uid)
    output = name + " 登录正常，开始学习...\n"

    article_index = user.get_article_index(uid)
    video_index = 1  # user.get_video_index(uid)

    total, scores = show_score(cookies)
    gl.pushprint(output, chat_id=uid)
    if TechXueXi_mode in ["1", "3"]:

        article_thread = threads.MyThread(
            "文章学 xi ", article, uid, cookies, article_index, scores, lock=lock)
        video_thread = threads.MyThread(
            "视频学 xi ", video, uid, cookies, video_index, scores, lock=lock)
        article_thread.start()
        video_thread.start()
        article_thread.join()
        video_thread.join()
    if TechXueXi_mode in ["2", "3"]:
        print('开始每日答题……')
        daily(cookies, scores)
        print('开始每周答题……')
        weekly(cookies, scores)
        if nohead != True or gl.zhuanxiang == True:
            print('开始专项答题……')
            zhuanxiang(cookies, scores)

    if TechXueXi_mode == "4":
        user.select_user()
    if TechXueXi_mode == "5":
        user.refresh_all_cookies(display_score=True)
    if TechXueXi_mode == "6":
        user.refresh_all_cookies(live_time=11.90)

    seconds_used = int(time.time() - start_time)
    gl.pushprint(name+" 总计用时 " + str(math.floor(seconds_used / 60)) +
                 " 分 " + str(seconds_used % 60) + " 秒", chat_id=uid)
    show_scorePush(cookies, chat_id=uid)
    try:
        user.shutdown(stime)
    except Exception as e:
        pass


def start(nick_name=None):
    nohead, lock, stime, Single = get_argv()
    info_shread = threads.MyThread("获取更新信息...", version.up_info)
    info_shread.start()
    user_list = user.list_user(printing=False)
    user.refresh_all_cookies()
    if len(user_list) == 0:
        user_list.append(["", "新用户"])
    for i in range(len(user_list)):
        try:
            if nick_name == None or nick_name == user_list[i][1] or nick_name == user_list[i][0]:
                _learn = threads.MyThread(
                    user_list[i][0]+"开始学xi", start_learn, user_list[i][0], user_list[i][1], lock=Single)
                _learn.start()
        except:
            gl.pushprint("学习页面崩溃，学习终止")


def get_my_score(uid):
    get_argv()
    user.refresh_all_cookies()
    cookies = user.get_cookie(uid)
    if not cookies:
        return False
    show_scorePush(cookies, chat_id=uid)
    return True


def get_user_list():
    get_argv()
    dic = user.refresh_all_cookies(display_score=True)
    values = dic.values()
    msg = ""
    for v in values:
        msg += v+"\n"
    if msg == "":
        msg = "cookie全部过期，请重新登录"
    return msg


def get_all_user_name():
    user_list = user.list_user(printing=False)
    names = []
    for i in range(len(user_list)):
        names.append(user_list[i][1])
    return names


def add_user(chat_id=None):
    get_argv()
    gl.pushprint("请登录（登录方式请仔细阅读文档，如果觉得这是让你下载，就是你没仔细读文档）：", chat_id=chat_id)
    driver_login = Mydriver()
    cookies = driver_login.login(chat_id)
    driver_login.quit()
    if not cookies:
        gl.pushprint("登录超时。", chat_id=chat_id)
        return
    user.save_cookies(cookies)
    uid = user.get_userId(cookies)
    user_fullname = user.get_fullname(uid)
    user.update_last_user(uid)
    gl.pushprint(user_fullname+"登录成功", chat_id=chat_id)


if __name__ == '__main__':
    if(cfg_get('display.banner') != False):  # banner文本直接硬编码，不要放在conf中
        print("=" * 60 +
              '\n    我们的网站，GitHub 等页面已经被中国大陆的浏览器加入黑名单，请用谷歌浏览器 chrome 打开我们的站点。' +
              '\n    科技强 guo 官方网站：https://techxuexi.js.org' +
              '\n    Github地址：https://github.com/TechXueXi' +
              '\n使用本项目，必须接受以下内容，否则请立即退出：' +
              '\n    - TechXueXi 仅额外提供给“爱党爱 guo ”且“工作学业繁重”的人' +
              '\n    - 项目开源协议 LGPL-3.0' +
              '\n    - 不得利用本项目盈利' +
              '\n另外，我们建议你参与一个维护劳动法的项目：' +
              '\nhttps://996.icu/ 或 https://github.com/996icu/996.ICU/blob/master/README_CN.md')
    print("=" * 60, '''\nTechXueXi 现支持以下模式（答题时请值守电脑旁处理少部分不正常的题目）：''')
    print(cfg_get('base.ModeText', "") + '\n' + "=" * 60)
    # 模式提示文字请在 ./config/default_template.conf 处修改。
    start()
