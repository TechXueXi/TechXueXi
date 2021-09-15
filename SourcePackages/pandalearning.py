import os
import sys
import time
import math
from sys import argv
from pdlearn import boot
boot.check_environment()
try:
    # 在此处导入所有 pdlearn 内的模块
    from pdlearn import version
    from pdlearn import user
    from pdlearn import score
    from pdlearn import color
    from pdlearn import threads
    from pdlearn.config          import cfg
    from pdlearn.mydriver        import Mydriver
    from pdlearn.score           import show_score
    from pdlearn.score           import show_scorePush
    from pdlearn.article_video   import article, video
    from pdlearn.answer_question import daily, weekly, zhuanxiang
    import pdlearn.globalvar as gl
except ImportError as e:
    boot.try_pip_install(exception=e)

def get_argv():
    nohead = False
    lock = False
    stime = False
    if os.getenv('Nohead') == "True":
        nohead=True
    if os.getenv('islooplogin') == "True":
        gl.islooplogin=True
    if len(argv) > 2:
        if argv[2] == "hidden":
            nohead = True
        elif argv[2] == "show":
            nohead = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    if os.getenv('AccessToken')==None:
        try:
            gl.accesstoken = cfg["addition"]["token"]
        except:
            gl.accesstoken=""
    else:
        gl.accesstoken=os.getenv('AccessToken')
    if os.getenv('Secret')==None:
        try:
            gl.secret = cfg["addition"]["secret"]
        except:
            gl.secret=""
    else:
        gl.secret=os.getenv('Secret')

    if os.getenv('Pushmode')==None:
        try:
            gl.pushmode=cfg["addition"]["Pushmode"]
        except:
            gl.pushmode="0"
    else:
        gl.pushmode=os.getenv('Pushmode')
    gl.nohead=nohead
    return nohead, lock, stime


if __name__ == '__main__':
    nohead, lock, stime = get_argv()
    print("是否无头模式：{0} {1}".format(nohead,os.getenv('Nohead')))
    #  0 读取版本信息
    start_time = time.time()
    if(cfg['display']['banner'] != False): # banner文本直接硬编码，不要放在conf中
        print("=" * 60 + \
        '\n    科技强 guo 官方网站：https://techxuexi.js.org' + \
        '\n    Github地址：https://github.com/TechXueXi' + \
        '\n使用本项目，必须接受以下内容，否则请立即退出：' + \
        '\n    - TechXueXi 仅额外提供给“爱党爱 guo ”且“工作学业繁重”的人' + \
        '\n    - 项目开源协议 LGPL-3.0' + \
        '\n    - 不得利用本项目盈利' + \
        '\n另外，我们建议你参与一个维护劳动法的项目：' + \
        '\nhttps://996.icu/ 或 https://github.com/996icu/996.ICU/blob/master/README_CN.md')
    cookies = user.check_default_user_cookie()
    user.list_user()
    user.refresh_all_cookies()
    print("=" * 60, '''\nTechXueXi 现支持以下模式（答题时请值守电脑旁处理少部分不正常的题目）：''')
    print(cfg['base']['ModeText'] + '\n' + "=" * 60) # 模式提示文字请在 ./config/default_template.conf 处修改。

    if nohead==True:
        TechXueXi_mode="3"
    else:
        try:
            if cfg["base"]["ModeType"]:
                print("默认选择模式：" + str(cfg["base"]["ModeType"]) + "\n" + "=" * 60)
                TechXueXi_mode = str(cfg["base"]["ModeType"])
        except Exception as e:
            TechXueXi_mode = input("请选择模式（输入对应数字）并回车： ")

    info_shread = threads.MyThread("获取更新信息...", version.up_info)
    info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    uid = user.get_default_userId()
    user_fullname=""
    if not cookies or TechXueXi_mode == "0":
        print("未找到有效登录信息，需要登录")
        driver_login = Mydriver()
        cookies = driver_login.login()
        driver_login.quit()
        user.save_cookies(cookies)
        uid = user.get_userId(cookies)
        user_fullname = user.get_fullname(uid)
        user.update_last_user(uid)
    # 增加多用户支持，已经有登录信息的重新扫码
    elif nohead==True:
        user_fullname = user.get_fullname(uid)
        output = "\n用户" + user_fullname + "已登录,如要再次学习请重新扫码\n"
        print(output)
        gl.pushprint(output)
        driver_login = Mydriver()
        cookies = driver_login.login()
        driver_login.quit()
        user.save_cookies(cookies)
        uid = user.get_userId(cookies)
        user.update_last_user(uid)
    output = "\n用户：" + user_fullname + "登录正常，开始学习...\n"

    article_index = user.get_article_index(uid)
    video_index = 1  # user.get_video_index(uid)

    total, scores = show_score(cookies)
    gl.pushprint(output)
    if TechXueXi_mode in ["1", "3"]:

        article_thread = threads.MyThread("文章学 xi ", article, uid, cookies, article_index, scores, lock=lock)
        video_thread = threads.MyThread("视频学 xi ", video, uid, cookies, video_index, scores, lock=lock)
        article_thread.start()
        video_thread.start()
        article_thread.join()
        video_thread.join()
    if TechXueXi_mode in ["2", "3"]:
        driver_default = Mydriver()
        print('开始每日答题……')
        daily(cookies, scores, driver_default=driver_default)
        if TechXueXi_mode in ["2", "3"]:
            print('开始每周答题……')
            weekly(cookies, scores, driver_default=driver_default)
            if nohead!=True:
                print('开始专项答题……')
                zhuanxiang(cookies, scores, driver_default=driver_default)
        try:
            driver_default.quit()
        except Exception as e:
            gl.pushprint('driver_default 在 main 退出时出了一点小问题...')
    if TechXueXi_mode == "4":
        user.select_user()
    if TechXueXi_mode == "5":
        user.refresh_all_cookies(display_score=True)
    if TechXueXi_mode == "6":
        user.refresh_all_cookies(live_time=11.90)

    seconds_used = int(time.time() - start_time)
    print("总计用时 " + str(math.floor(seconds_used / 60)) + " 分 " + str(seconds_used % 60) + " 秒")
    show_scorePush(cookies)
    try:
        user.shutdown(stime)
    except Exception as e:
        pass
