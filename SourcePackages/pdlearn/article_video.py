import time
import random
from pdlearn import user
from pdlearn import color
from pdlearn import threads
from pdlearn import get_links
from pdlearn.mydriver import Mydriver
from pdlearn.score import show_score
from pdlearn.const import const


def article(userId, cookies, article_pointer, scores):
    try:
        if scores["article_num"] < const.article_num_all or scores["article_time"] < const.article_time_all:
            # driver_article = Mydriver(nohead=nohead)
            driver_article = Mydriver(nohead=True)
            # def article_stop_function():
            #     driver_article.quit()
            # threads.regist_stop_function(article_stop_function)
            driver_article.get_url("https://www.xuexi.cn/notFound.html")
            driver_article.set_cookies(cookies)
            links = get_links.get_article_links()
            try_count = 0
            readarticle_time = 0
            while True:
                if scores["article_num"] < const.article_num_all and try_count < 10:
                    article_remain = const.article_num_all - scores["article_num"]
                    for i in range(article_pointer, article_pointer + article_remain):
                        driver_article.get_url(links[i])
                        readarticle_time = 60 + random.randint(5, 15)
                        for j in range(readarticle_time):
                            if random.random() > 0.5:
                                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                            print("\r文章数量学 xi 中，文章剩余{}篇,本篇剩余时间{}秒".format(article_pointer + article_remain - i, readarticle_time - j), end="")
                            time.sleep(1)
                        driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                        total, scores = show_score(cookies)
                        if scores["article_num"] >= const.article_num_all:
                            print("检测到文章数量分数已满,退出学 xi ")
                            break
                    article_pointer += article_remain
                else:
                    user.save_article_index(userId, article_pointer)
                    break
            try_count = 0
            while True:
                if scores["article_time"] < const.article_time_all and try_count < 10:
                    num_time = 60
                    driver_article.get_url(links[article_pointer - 1])
                    remaining = (const.article_time_all - scores["article_time"]) * 1 * num_time
                    for i in range(remaining):
                        if random.random() > 0.5:
                            driver_article.go_js(
                                'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                        print("\r文章时长学 xi 中，文章总时长剩余{}秒".format(remaining - i), end="")
                        time.sleep(1)
                        if i % (60) == 0 and i != remaining:
                            total, scores = show_score(cookies)
                            if scores["article_time"] >= const.article_time_all:
                                print("检测到文章时长分数已满,退出学 xi ")
                                break
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, scores = show_score(cookies)
                else:
                    break
            if try_count < 10:
                print("文章学 xi 完成")
            else:
                print("文章学 xi 出现异常，请检查 user/article_video_index.json 文件记录")
            driver_article.quit()
        else:
            print("文章之前学完了")
    except Exception as e:
        print(color.red("文章学 xi 检测到异常："+str(e)))


def video(userId, cookies, video_pointer, scores):
    try:
        if scores["video_num"] < const.video_num_all or scores["video_time"] < const.video_time_all:
            # driver_video = Mydriver(nohead=nohead)
            driver_video = Mydriver(nohead=True)
            # def video_stop_function():
            #     driver_video.quit()
            # threads.regist_stop_function(video_stop_function)
            driver_video.get_url("https://www.xuexi.cn/notFound.html")
            driver_video.set_cookies(cookies)
            links = get_links.get_video_links()
            try_count = 0
            watchvideo_time = 0
            while True:
                if scores["video_num"] < const.video_num_all and try_count < 10:
                    v_num = const.video_num_all - scores["video_num"]
                    for i in range(video_pointer, video_pointer + v_num):
                        driver_video.get_url(links[i])
                        watchvideo_time = 60 + random.randint(5, 15)
                        for j in range(watchvideo_time):
                            if random.random() > 0.5:
                                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                            print("\r视频数量学 xi 中，视频剩余{}个,本次剩余时间{}秒".format(video_pointer + v_num - i, watchvideo_time - j), end="")
                            time.sleep(1)
                        driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                        total, scores = show_score(cookies)
                        if scores["video_num"] >= const.video_num_all:
                            print("检测到视频数量分数已满,退出学 xi ")
                            break
                    video_pointer += v_num
                else:
                    user.save_video_index(userId, video_pointer)
                    break
            try_count = 0
            while True:
                if scores["video_time"] < const.video_time_all and try_count < 10:
                    num_time = 60
                    driver_video.get_url(links[video_pointer - 1])
                    remaining = (const.video_time_all - scores["video_time"]) * 1 * num_time
                    for i in range(remaining):
                        if random.random() > 0.5:
                            driver_video.go_js(
                                'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                        print("\r视频时长学 xi 中，视频总时长剩余{}秒".format(remaining - i), end="")
                        time.sleep(1)
                        if i % (60) == 0 and i != remaining:
                            total, scores = show_score(cookies)
                            if scores["video_time"] >= const.video_time_all:
                                print("检测到视频时长分数已满,退出学 xi ")
                                break
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, scores = show_score(cookies)
                else:
                    break
            if try_count < 10:
                print("视频学 xi 完成")
            else:
                print("视频学 xi 出现异常，请检查 user/article_video_index.json 文件记录")
            driver_video.quit()
        else:
            print("视频之前学完了")
    except Exception as e:
        print(color.red("视频学 xi 检测到异常："+str(e)))
