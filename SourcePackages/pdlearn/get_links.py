import requests
import re
import random
import json


def get_article_links():
    try:
        article = requests.get(
            "https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/data9a3668c13f6e303932b5e0e100fc248b.js").content.decode(
            "utf8")
        pattern = r"list\"\:(.+),\"count\"\:"
        links = []
        list = eval(re.search(pattern, article).group(1))[:20000]
        list.reverse()
        for i in range(len(list)):
            links.append(list[i]["static_page_url"])
        return links
    except:
        print("=" * 60)
        print("get_article_links获取失败")
        print("=" * 60)
        raise


def get_video_links():
    try:
        # 解决视频不能正常学习的问题
        video_json = requests.get(
            "https://www.xuexi.cn/lgdata/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.json").content.decode(
            "utf8")
        video = json.loads(video_json)["DataSet"]
        json_urls = []
        for i in video:
            json_urls.append("https://www.xuexi.cn/lgdata/" + i.split('!')[1])

        all_video_object = []
        for url in json_urls:
            choose_json_str = requests.get(url).content.decode("utf8")
            all_video_object.extend(json.loads(choose_json_str))
        new_list = sorted(all_video_object, key=lambda x: x.get("publishTime", "0"), reverse=False)
        return [news["url"] for news in new_list]
    except:
        print("=" * 60)
        print("get_video_links获取失败")
        print("=" * 60)
        raise
