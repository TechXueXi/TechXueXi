import os
import sys
import time
import math
from sys import argv
from pdlearn import version
from pdlearn import user
from pdlearn import score
from pdlearn import color
from pdlearn import threads
from pdlearn.config          import cfg
from pdlearn.mydriver        import Mydriver
from pdlearn.score           import show_score, get_score_output
from pdlearn.article_video   import article, video
from pdlearn.answer_question import daily, weekly, zhuanxiang
from pdlearn.dingding import DingDingHandler
from pdlearn.timeout import timeout, TimeoutError


def get_argv():
    assert len(argv) == 3, '参数错误，例：python pandalearning.py 替换为自己的token 替换为自己的secret'
    token = argv[1]
    secret = argv[2]
    return token, secret


@timeout(1800, 'timeout')
def answer_question(cookies, scores):
    TechXueXi_mode = "3"
    if TechXueXi_mode in ["2", "3"]:
        print('开始每日答题……')
        daily(cookies, scores)
    if TechXueXi_mode in ["3"]:
        print('开始每周答题……')
        weekly(cookies, scores)
        print('开始专项答题……')
        zhuanxiang(cookies, scores)


if __name__ == '__main__':
    # 注：不要再pandalearning.py之外使用os.chdir(sys.path[0])，否则可能造成打包程序不能运行
    # 切换pwd到python文件路径，避免找不到相对路径下的ini和相关文件
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(base_path)
    #  0 读取版本信息
    start_time = time.time()
    if(cfg['display']['banner'] != "false"): # banner文本直接硬编码，不要放在ini中
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
    # user.select_user()
    # print("=" * 60, '''\nTechXueXi 现支持以下模式（答题时请值守电脑旁处理少部分不正常的题目）：''')
    # print(cfg['base']['ModeText'] + '\n' + "=" * 60) # 模式提示文字请在 ./config/main.ini 处修改。
    #
    # try:
    #     if cfg["base"]["ModeType"]:
    #         print("默认选择模式：" + cfg["base"]["ModeType"] + "\n" + "=" * 60)
    #         TechXueXi_mode = cfg["base"]["ModeType"]
    # except Exception as e:
    #     TechXueXi_mode = input("请选择模式（输入对应数字）并回车： ")
    token, secret = get_argv()
    ddhandler = DingDingHandler(token, secret)
    info_shread = threads.MyThread("获取更新信息...", version.up_info)
    info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    uid = user.get_default_userId()
    if not cookies:
        print("未找到有效登录信息，需要登录")
        driver_login = Mydriver(nohead=True, ddhandler=ddhandler)
        cookies = driver_login.login()
        driver_login.quit()
        user.save_cookies(cookies)
        uid = user.get_userId(cookies)
        user_fullname = user.get_fullname(uid)
        user.update_last_user(uid)
    article_index = user.get_article_index(uid)
    video_index = user.get_video_index(uid)

    total, scores = show_score(cookies)

    lock = False
    article_thread = threads.MyMainThread("文章学 xi ", article, uid, cookies, article_index, scores, lock=lock)
    video_thread = threads.MyMainThread("视频学 xi ", video, uid, cookies, video_index, scores, lock=lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()
    try:
        answer_question(cookies, scores)
    except TimeoutError:
        print('答题超时退出')

    seconds_used = int(time.time() - start_time)
    print("总计用时 " + str(math.floor(seconds_used / 60)) + " 分 " + str(seconds_used % 60) + " 秒")
    output = get_score_output(cookies)
    output += "\n总计用时 " + str(math.floor(seconds_used / 60)) + " 分 " + str(seconds_used % 60) + " 秒"
    ddhandler.ddtextsend(output)

    stime = 0
    user.shutdown(stime)
