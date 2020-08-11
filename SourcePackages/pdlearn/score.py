import requests
from requests.cookies import RequestsCookieJar
import json


def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar).content.decode("utf8")
        total = int(json.loads(total, encoding="utf8")["data"]["score"])
        each = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar).content.decode(
            "utf8")
        each = json.loads(each, encoding="utf8")["data"]["dayScoreDtos"]
        each = [int(i["currentScore"]) for i in each if i["ruleId"] in [1, 2, 9, 1002, 1003]]
        return total, each
    except:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise
