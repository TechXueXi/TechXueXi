import requests
from requests.cookies import RequestsCookieJar
import json
from pdlearn.const import const


# 总积分
# https://pc-api.xuexi.cn/open/api/score/get?_t=1608769882241
# 今日积分
# https://pc-api.xuexi.cn/open/api/score/today/query


def show_score(cookies):
    userId, total, scores = get_score(cookies)
    print("当前学 xi 总积分：" + str(total) + "\t" + "今日得分：" + str(scores["today"]))
    print("阅读文章:", scores["article_num"], "/", const.article_num_all, ",",
        "观看视频:", scores["video_num"], "/", const.video_num_all, ",",
        "文章时长:", scores["article_time"], "/", const.article_time_all, ",",
        "视频时长:", scores["video_time"], "/", const.video_time_all, ",",
        "\n每日登陆:", scores["login"], "/", const.login_all, ",",
        "每日答题:", scores["daily"], "/", const.daily_all, ",",
        "每周答题:", scores["weekly"], "/", const.weekly_all, ",",
        "专项答题:", scores["zhuanxiang"], "/", const.zhuanxiang_all)
    return total, scores


def get_score_output(cookies):
    userId, total, scores = get_score(cookies)
    output = "当前学 xi 总积分：" + str(total) + "\t" + "今日得分：" + str(scores["today"])
    output += "\n阅读文章:" + str(scores["article_num"]) + "/" + str(const.article_num_all) + \
              "\n观看视频:" + str(scores["video_num"]) + "/" + str(const.video_num_all) + \
              "\n文章时长:" + str(scores["article_time"]) + "/" + str(const.article_time_all) + \
              "\n视频时长:" + str(scores["video_time"]) + "/" + str(const.video_time_all) + \
              "\n每日登陆:" + str(scores["login"]) + "/" + str(const.login_all) + \
              "\n每日答题:" + str(scores["daily"]) + "/" + str(const.daily_all) + \
              "\n每周答题:" + str(scores["weekly"]) + "/" + str(const.weekly_all) + \
              "\n专项答题:" + str(scores["zhuanxiang"]) + "/" + str(const.zhuanxiang_all)
    return output


def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total_json = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar,
                                  headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        total = int(json.loads(total_json)["data"]["score"])
        userId = json.loads(total_json)["data"]["userId"]
        score_json = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar,
                                  headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        today_json = requests.get("https://pc-api.xuexi.cn/open/api/score/today/query", cookies=jar,
                                  headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        today = 0
        today = int(json.loads(today_json)["data"]["score"])
        dayScoreDtos = json.loads(score_json)["data"]["dayScoreDtos"]
        rule_list = [1, 2, 9, 1002, 1003, 6, 5, 4]
        score_list= [0, 0, 0, 0   , 0   , 0, 0, 0, 0, 0] # 长度为十
        for i in dayScoreDtos:
            for j in range(len(rule_list)):
                if i["ruleId"] == rule_list[j]:
                    score_list[j] = int(i["currentScore"])
        # 阅读文章，视听学 xi ，登录，文章时长，视听学 xi 时长，每日答题，每周答题，专项答题
        scores = {}
        scores["article_num"]  = score_list[0] # 0阅读文章
        scores["video_num"]    = score_list[1] # 1视听学 xi
        scores["login"]        = score_list[2] # 7登录
        scores["article_time"] = score_list[3] # 6文章时长
        scores["video_time"]   = score_list[4] # 5视听学 xi 时长
        scores["daily"]        = score_list[5] # 2每日答题
        scores["weekly"]       = score_list[6] # 3每周答题
        scores["zhuanxiang"]   = score_list[7] # 4专项答题

        scores["today"]        = today         # 8今日得分
        return userId ,total, scores
    except:
        print("=" * 60)
        print("get_score 获取失败")
        print("=" * 60)
        raise
