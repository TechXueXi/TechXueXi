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
        video_json = requests.get("https://www.xuexi.cn/lgdata/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.json").content.decode("utf8")
        video=json.loads(video_json)["DataSet"]
        json_urls = []
        link = []
        for i in video:
            json_urls.append("https://www.xuexi.cn/lgdata/"+i.split('!')[1])
        while len(link) < 20:
            choose_json_url = random.choice(json_urls)
            choose_json_str = requests.get(choose_json_url).content.decode("utf8")
            pattern = r'https://www.xuexi.cn/[^,"]*'
            choose_links = re.findall(pattern, choose_json_str, re.I)
            if(len(choose_links) >= 5):
                choose_sample = random.sample(choose_links, 5)
                for c in choose_sample:
                    link.append(c)
        random.shuffle(link)
        return link
    except:
        print("=" * 60)
        print("get_video_links获取失败")
        print("=" * 60)
        raise
