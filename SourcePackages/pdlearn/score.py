from pickle import TRUE
from pdlearn import globalvar
import requests
from requests.cookies import RequestsCookieJar
import json
from pdlearn import color
from pdlearn import file
from pdlearn.const import const
import threading


# 总积分
# https://pc-api.xuexi.cn/open/api/score/get?_t=1608769882241
# 今日积分
# https://pc-api.xuexi.cn/open/api/score/today/query


def handle_score_color(score, full_score, colorful=True):
    if int(score) < int(full_score) and colorful:
        return color.red(str(score))+" / "+str(full_score)
    else:
        return str(score)+" / "+str(full_score)


def show_score(cookies):
    userId, total, scores, userName = get_score(cookies)
    print(userName+" 当前学 xi 总积分：" + str(total) +
          "\t" + "今日得分：" + str(scores["today"]))
    print("阅读文章:", handle_score_color(scores["article_num"], const.article_num_all), ",",
          "观看视频:", handle_score_color(
              scores["video_num"], const.video_num_all), ",",
          "文章时长:", handle_score_color(
              scores["article_time"], const.article_time_all), ",",
          "视频时长:", handle_score_color(
              scores["video_time"], const.video_time_all), ",",
          "\n每日登陆:", handle_score_color(scores["login"], const.login_all), ",",
          "每日答题:", handle_score_color(scores["daily"], const.daily_all), ",",
          "每周答题:", handle_score_color(scores["weekly"], const.weekly_all), ",",
          "专项答题:", handle_score_color(scores["zhuanxiang"], const.zhuanxiang_all))
    return total, scores


def show_scorePush(cookies, chat_id=None):
    userId, total, scores, userName = get_score(cookies)
    globalvar.pushprint(userName+" 当前学 xi 总积分：" + str(total) + "\t" + "今日得分：" + str(scores["today"]) +
                        "\n阅读文章:" + handle_score_color(scores["article_num"], const.article_num_all, False) + "," +
                        "观看视频:" + handle_score_color(scores["video_num"], const.video_num_all, False) + "," +
                        "文章时长:" + handle_score_color(scores["article_time"], const.article_time_all, False) + "," +
                        "视频时长:" + handle_score_color(scores["video_time"], const.video_time_all, False) + "," +
                        "\n每日登陆:" + handle_score_color(scores["login"], const.login_all, False) + "," +
                        "每日答题:" + handle_score_color(scores["daily"], const.daily_all, False) + "," +
                        "每周答题:" + handle_score_color(scores["weekly"], const.weekly_all, False) + "," +
                        "专项答题:" + handle_score_color(scores["zhuanxiang"], const.zhuanxiang_all, False), chat_id)
    return total, scores


def get_score(cookies):
    chat_id = None
    th_name = threading.current_thread().name
    if "开始学xi" in th_name:
        chat_id = th_name[:th_name.index("开始学xi")]
    requests.adapters.DEFAULT_RETRIES = 5
    jar = RequestsCookieJar()
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])
    total_json = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar,
                              headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    if not json.loads(total_json)["data"]:
        globalvar.pushprint("cookie过期，请重新登录", chat_id)
        if chat_id:
            remove_cookie(chat_id)
        raise

    total = int(json.loads(total_json)["data"]["score"])
    #userId = json.loads(total_json)["data"]["userId"]
    user_info = requests.get("https://pc-api.xuexi.cn/open/api/user/info", cookies=jar,
                             headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    userId = json.loads(user_info)["data"]["uid"]
    userName = json.loads(user_info)["data"]["nick"]
    # score_json = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar,
    #                          headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    # today_json = requests.get("https://pc-api.xuexi.cn/open/api/score/today/query", cookies=jar,
    #                          headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    today = 0
    # today = int(json.loads(today_json)["data"]["score"])
    score_json = requests.get("https://pc-proxy-api.xuexi.cn/api/score/days/listScoreProgress?sence=score&deviceType=2", cookies=jar,
                              headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    dayScoreDtos = json.loads(score_json)["data"]
    today = dayScoreDtos["totalScore"]
    rule_list = [1, 2, 9, 1002, 1003, 6, 5, 4]
    score_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 长度为十
    for i in dayScoreDtos["taskProgress"]:
        for j in range(len(rule_list)):
            if str(rule_list[j]) in i["taskCode"]:
                score_list[j] = int(
                    int(i["currentScore"])/len(i["taskCode"]))
    # 阅读文章，视听学 xi ，登录，文章时长，视听学 xi 时长，每日答题，每周答题，专项答题
    scores = {}
    scores["article_num"] = score_list[0]  # 0阅读文章
    scores["video_num"] = score_list[1]  # 1视听学 xi
    scores["login"] = score_list[2]  # 7登录
    scores["article_time"] = score_list[3]  # 6文章时长
    scores["video_time"] = score_list[4]  # 5视听学 xi 时长
    scores["daily"] = score_list[5]  # 2每日答题
    scores["weekly"] = score_list[6]  # 3每周答题
    scores["zhuanxiang"] = score_list[7]  # 4专项答题

    scores["today"] = today         # 8今日得分
    return userId, total, scores, userName


def remove_cookie(uid):
    template_json_str = '''{}'''
    cookies_json_obj = file.get_json_data(
        "user/cookies.json", template_json_str)
    cookies_json_obj.pop(str(uid))
    file.save_json_data("user/cookies.json", cookies_json_obj)
