import requests
import re


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
        print("=" * 120)
        print("get_article_links获取失败")
        print("=" * 120)
        raise


def get_video_links():
    try:
        video = requests.get(
            "https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js").content.decode(
            "utf8")
        pattern = r'https://www.xuexi.cn/[^,"]*html'
        link = re.findall(pattern, video, re.I)
        link.reverse()
        return link
    except:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise
