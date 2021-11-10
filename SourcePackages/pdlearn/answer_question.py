from pdlearn import globalvar
import time
import random
from pdlearn import auto
from pdlearn import user
from pdlearn import color
from pdlearn.mydriver import Mydriver
from pdlearn.score import show_score
from pdlearn.const import const
from pdlearn.log import *
from pdlearn.config import cfg_get
from pdlearn.exp_catch import exception_catcher
from pdlearn.db_helper import search_answer
from pdlearn import globalvar as gl


def generate_tiku_data(quiz_type=None, tip=None, option=None, answer=None, question=None):
    """
    需要信息：题目类型、题干html、题干文本、tips html、tips文本、选项列表（选择题）、视频链接（视频题）
    """
    data = '{quiz_type:'+quiz_type+',tip:'+tip+',option:' + \
        option+',answer:'+answer+',question:'+question+'}'
    return data


def find_available_quiz(quiz_type, driver_ans, uid):
    pages = driver_ans.driver.find_elements_by_css_selector(
        ".ant-pagination-item")
    for p in range(0, len(pages), 1):  # (从最后一页开始往前找做题)从前往后找题，专项答题等没有那么离谱
        time.sleep(0.5)
        print('进入答题第' + str(p+1) + '页')
        pages[p].click()
        time.sleep(0.5)
        dati = []
        if quiz_type == "weekly":  # 寻找可以做的题
            dati = driver_ans.driver.find_elements_by_css_selector(
                "#app .month .week button")
        elif quiz_type == "zhuanxiang":  # 寻找可以做的题
            # 可以使用 #app .items .item button:not(.ant-btn-background-ghost) 选择器，但会遗漏掉”继续答题“的部分
            dati = driver_ans.driver.find_elements_by_css_selector(
                "#app .items .item button")
        for i in range(len(dati)-1, -1, -1):  # 从最后一个遍历到第一个
            j = dati[i]
            if ("重新" in j.text or "满分" in j.text):
                continue
            else:
                to_click = j
                # auto.prompt("wait for Enter press...")
                return to_click


@exception_catcher()
def answer_question(quiz_type, cookies, scores, score_all, quiz_xpath, category_xpath, uid=None, driver_default=None):
    quiz_zh_CN = {"daily": "每日", "weekly": "每周", "zhuanxiang": "专项"}
    if(quiz_type not in ["daily", "weekly", "zhuanxiang"]):
        print("quiz_type 错误。收到的quiz_type："+quiz_type)
        exit(0)
    if uid is None:
        uid = user.get_userId(cookies)
    if scores[quiz_type] < score_all:  # 还没有满分，需要答题
        if driver_default is None:
            driver_ans = Mydriver(nohead=gl.nohead)
            ##### driver_ans = Mydriver(nohead=True)
        else:
            driver_ans = driver_default
        driver_daily = driver_ans
        driver_weekly = driver_ans
        driver_zhuanxiang = driver_ans
        # try:
        #     nohead = gl.nohead
        # except:
        #     nohead=False
        # if nohead:
        #     print("使用默认窗口大小")
        # else:
        driver_ans.driver.maximize_window()
        print('请保持窗口最大化\n'*3)
        driver_ans.get_url("https://www.xuexi.cn/notFound.html")
        driver_ans.set_cookies(cookies)
        pass_count = 0
        # 最大值，用于nohead模式退出
        max_count = 0
        # 从数据库获取答案
        answer_from_db = False
        answer_error_max = cfg_get("parameter.answer_error_max", 100)
        # 是否开启错题收集
        answer_error_collect = cfg_get("parameter.answer_error_collect", True)
        if scores[quiz_type] < score_all:
            letters = list("ABCDEFGHIJKLMN")
            driver_ans.get_url('https://pc.xuexi.cn/points/my-points.html')
            refresh_my_page_count = 0
            # 页面title为积分则一直循环
            while driver_ans.title_is(u"我的积分") and refresh_my_page_count < 20:
                time.sleep(1)  # 等待页面刷新提示
                refresh_buttons = driver_ans.driver.find_elements_by_css_selector(
                    ".ant-modal-wrap .ant-btn:not(.ant-btn-primary)")
                if len(refresh_buttons) > 0:  #
                    refresh_buttons[0].click()
                driver_ans.click_xpath(quiz_xpath)  # 点击各个题目的去答题按钮
                time.sleep(1)
                refresh_my_page_count += 1
                if refresh_my_page_count >= 20:
                    print("没有找到答题按钮")
            if quiz_type != "daily":  # 如果是每日答题就不用找available了
                # 此处修改是因为页面可能刷新后导致的查找元素button 丢失从而引发异常重新此处用可以重新查找来解决
                try:
                    to_click = find_available_quiz(quiz_type, driver_ans, uid)
                except Exception as e:
                    to_click = find_available_quiz(quiz_type, driver_ans, uid)
                if to_click is not None:
                    to_click.click()
                    time.sleep(0.5)
                else:
                    print(color.blue("无题可答。即将跳过。"))
                    if driver_default is None:
                        try:
                            driver_ans.quit()
                        except Exception as e:
                            print('driver_ans 在 answer_question 退出时出了一点小问题...')
                    else:
                        pass  # 其他函数传入函数的driver，不自动退出
            while scores[quiz_type] < score_all:
                try:
                    category = driver_ans.xpath_getText(
                        category_xpath)  # 获取题目类型 get_attribute("name")
                except Exception as e:
                    print('查找题目类型...查找元素失败！')
                    break
                # 全局出错次数
                if max_count >= answer_error_max and globalvar.nohead == True:
                    print("略过次数已经超过"+str(answer_error_max) +
                          "次，且出于Nohead模式，退出答题")
                    break
                print(category)
                q_text = ""
                tips = []
                tip_full_text = ""
                if quiz_type == "daily":
                    ans_results = driver_ans.driver.find_elements_by_css_selector(
                        ".practice-result .infos .info")
                    if(len(ans_results) != 0):  # 已经找到答题结果页面
                        print(ans_results[0].get_attribute("innerHTML"))
                        print(ans_results[0].text)
                        print(ans_results[2].get_attribute("innerHTML"))
                        print(ans_results[2].text)
                        time.sleep(1)
                        # exit(2)
                        break
                    log_daily("\n====================")
                    log_daily(log_timestamp())
                try:
                    log_daily("【"+category+"】")
                    log_daily("【题干】")
                    q_body = driver_ans.driver.find_element_by_css_selector(
                        ".q-body")
                    q_html = q_body.get_attribute('innerHTML')
                    q_text = q_body.text
                    print(q_text)
                    log_daily(q_html)
                except Exception as e:
                    print("获取题干出错"+str(e))
                # 上次出错，则采用数据库答题
                if answer_from_db:
                    answer_from_db = False  # 下次从页面获取提示
                    try:
                        if not q_text:
                            q_body = driver_ans.driver.find_element_by_css_selector(
                                ".q-body")
                            q_html = q_body.get_attribute('innerHTML')
                            q_text = q_body.text
                        tips = search_answer(q_text)
                    except Exception as e:
                        print("数据搜索答案异常："+str(e))
                else:
                    tips, tip_full_text = driver_ans._view_tips()

                if quiz_type == "daily":
                    log_daily("【提示信息】")
                    log_daily(str(tips)+"\n"+tip_full_text)
                if not tips:
                    print("页面未找到提示，尝试从题库搜索答案。\n")
                    try:
                        answer_from_db = False  # 下次从页面获取提示
                        if not q_text:
                            q_body = driver_ans.driver.find_element_by_css_selector(
                                ".q-body")
                            q_html = q_body.get_attribute('innerHTML')
                            q_text = q_body.text
                        tips = search_answer(q_text)
                    except Exception as e:
                        print("数据搜索答案异常："+str(e))
                if not tips:
                    print("本题没有提示")
                    max_count += 1
                    pass_count += 1

                    if pass_count >= 5:
                        print(
                            "暂时略过已达到 5 次，【 建议您将此题目的题干、提示、选项信息提交到github问题收集issue：https://github.com/TechXueXi/techxuexi-tiku/issues/1 】")
                        auto.prompt("等待用户手动答题...完成后请在此按回车...")
                        pass_count = 0
                        continue
                    # if quiz_type == "daily":
                    #     log_daily("！！！！！本题没有找到提示，暂时略过！！！！！")
                    #     auto.prompt("等待用户手动答题...完成后请在此按回车...")
                    #     time.sleep(1)
                    #     continue
                    if "填空题" in category:
                        print('没有找到提示，暂时略过')
                        # print('使用默认答案  好 ')   #如无填空答案，使用默认答案 好 字 by Sean
                        ##### tips = ['好']
                        if gl.nohead and answer_error_collect:
                            gl.push_msg += "[题干]"+q_text+'\n'
                        continue
                    elif "多选题" in category:
                        print('没有找到提示，多选题默认全选')
                        # print('使用默认答案 全选')    #by Sean
                        ## continue  #####
                        tips = driver_daily.radio_get_options()
                        if gl.nohead and answer_error_collect:
                            gl.push_msg += f"[题干]{q_text}\n[选项]{str(tips)}\n"
                    elif "单选题" in category:
                        print('没有找到提示，单选题默认选A')  # 如无单选答案，使用默认答案
                        # print('使用默认答案 B')   #by Sean
                        # continue  #####
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                        ops = driver_daily.radio_get_options()
                        tips = [ops[0]]
                        if gl.nohead and answer_error_collect:
                            gl.push_msg += f"[题干]{q_text}\n[选项]{str(ops)}\n"
                    else:
                        print("题目类型非法")
                        if quiz_type == "daily":
                            log_daily("！！！！！无提示，题目类型非法！！！！！")
                        break
                if tips:
                    if "填空题" in category:
                        answer = tips
                        if quiz_type != "zhuanxiang":
                            driver_ans.fill_in_blank(answer)
                        else:
                            driver_ans.zhuanxiang_fill_in_blank(answer)
                    elif "多选题" in category:
                        if quiz_type == "daily":
                            options = driver_daily.radio_get_options()
                            ##### len_option = len(options)
                            log_daily("【多选题选项】")
                            log_daily(str(options))
                            radio_in_tips, radio_out_tips = "", ""
                            for letter, option in zip(letters, options):
                                for tip in tips:
                                    if tip in option:
                                        # print(f'{option} in tips')
                                        if letter not in radio_in_tips:
                                            radio_in_tips += letter
                            radio_out_tips = [letter for letter, option in zip(letters, options) if
                                              (letter not in radio_in_tips)]

                            print('包含提示的选项 ', radio_in_tips,
                                  '，不包含提示的选项 ', radio_out_tips)
                            log_daily('包含提示的选项 '+str(radio_in_tips) +
                                      '，不包含提示的选项 '+str(radio_out_tips))
                            # and radio_in_tips not in driver_daily.excludes:
                            if len(radio_in_tips) > 1:
                                print('根据提示', radio_in_tips)
                                driver_daily.radio_check(radio_in_tips)
                            elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                                print('根据提示', radio_out_tips)
                                driver_daily.radio_check(radio_out_tips)
                            # return driver_daily._search(content, options, excludes)
                            else:
                                max_count += 1
                                answer_from_db = True
                                print('无法根据提示判断，将在数据库中查询答案……')
                                log_daily("！！！！！无法根据提示判断，请自行答题……！！！！！")
                                # print('将使用默认全选答题')     #by Sean
                                ##### len_option = len(options)
                                ##### radio_in_tips = letters[:len_option]
                                # driver_daily.radio_check(radio_in_tips)
                                if not gl.nohead:
                                    auto.prompt("等待用户手动答题...完成后请在此按回车...")
                        elif quiz_type == "weekly":
                            options = driver_weekly.radio_get_options()
                            radio_in_tips, radio_out_tips = "", ""
                            for letter, option in zip(letters, options):
                                for tip in tips:
                                    if tip in option:
                                        # print(f'{option} in tips')
                                        if letter not in radio_in_tips:
                                            radio_in_tips += letter
                            radio_out_tips = [letter for letter, option in zip(letters, options) if
                                              (letter not in radio_in_tips)]

                            print('含 ', radio_in_tips, '不含', radio_out_tips)
                            # and radio_in_tips not in driver_weekly.excludes:
                            if len(radio_in_tips) > 1:
                                print('根据提示', radio_in_tips)
                                driver_weekly.radio_check(radio_in_tips)
                            elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                                print('根据提示', radio_out_tips)
                                driver_weekly.radio_check(radio_out_tips)
                            # return driver_weekly._search(content, options, excludes)
                            else:
                                max_count += 1
                                answer_from_db = True
                                print('无法根据提示判断，将在数据库中查询答案……')
                                # print('将使用默认全选答题')     #by Sean
                                ##### len_option = len(options)
                                ##### radio_in_tips = letters[:len_option]
                                # driver_weekly.radio_check(radio_in_tips)
                                if not gl.nohead:
                                    auto.prompt("等待用户手动答题...完成后请在此按回车...")
                        elif quiz_type == "zhuanxiang":
                            options = driver_zhuanxiang.radio_get_options()
                            radio_in_tips, radio_out_tips = "", ""
                            for letter, option in zip(letters, options):
                                for tip in tips:
                                    if tip in option:
                                        # print(f'{option} in tips')
                                        if letter not in radio_in_tips:
                                            radio_in_tips += letter
                            radio_out_tips = [letter for letter, option in zip(letters, options) if
                                              (letter not in radio_in_tips)]

                            print('含 ', radio_in_tips, '不含', radio_out_tips)
                            # and radio_in_tips not in driver_zhuanxiang.excludes:
                            if len(radio_in_tips) > 1:
                                print('根据提示', radio_in_tips)
                                driver_zhuanxiang.radio_check(radio_in_tips)
                            elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                                print('根据提示', radio_out_tips)
                                driver_zhuanxiang.radio_check(radio_out_tips)
                            # return driver_zhuanxiang._search(content, options, excludes)
                            else:
                                max_count += 1
                                answer_from_db = True
                                print('无法根据提示判断，将在数据库中查询答案……')
                                # print('将使用默认全选答题')     #by Sean
                                ##### len_option = len(options)
                                ##### radio_in_tips = letters[:len_option]
                                # driver_zhuanxiang.radio_check(radio_in_tips)
                                if not gl.nohead:
                                    auto.prompt("等待用户手动答题...完成后请在此按回车...")
                    elif "单选题" in category:
                        if quiz_type == "daily":
                            options = driver_daily.radio_get_options()
                            log_daily("【单选题选项】")
                            log_daily(str(options))
                            if '因此本题选' in tips:  # 提示类型1
                                check = [x for x in letters if x in tips]
                                log_daily("根据提示类型1，选择答案："+str(check))
                                driver_daily.radio_check(check)
                            else:
                                radio_in_tips, radio_out_tips = "", ""
                                '''
                                option_elements = driver_daily.wait.until(driver_daily.EC.presence_of_all_elements_located(
                                    (driver_daily.By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]')))
                                # option_elements = self.find_elements(rules['challenge_options'])
                                options = [x.get_attribute("name") for x in option_elements]'''
                                for letter, option in zip(letters, options):
                                    for tip in tips:
                                        if tip in option:
                                            # print(f'{option} in tips')
                                            if letter not in radio_in_tips:
                                                radio_in_tips += letter
                                        else:
                                            # print(f'{option} out tips')
                                            if letter not in radio_out_tips:
                                                radio_out_tips += letter

                                print('包含提示的选项 ', radio_in_tips,
                                      '，不包含提示的选项 ', radio_out_tips)
                                log_daily('包含提示的选项 '+str(radio_in_tips) +
                                          '，不包含提示的选项 '+str(radio_out_tips))
                                # and radio_in_tips not in driver_daily.excludes:
                                if 1 == len(radio_in_tips):
                                    print('根据提示', radio_in_tips)
                                    driver_daily.radio_check(radio_in_tips)
                                # and radio_out_tips not in excludes
                                elif 1 == len(radio_out_tips):
                                    print('根据提示', radio_out_tips)
                                    driver_daily.radio_check(radio_out_tips)
                                # return driver_daily._search(content, options, excludes)
                                else:
                                    max_count += 1
                                    answer_from_db = True
                                    print('无法根据提示判断，将在数据库中查询答案……')
                                    log_daily("！！！！！无法根据提示判断，请自行答题……！！！！！")
                                    # print('将使用默认选 B')     #by Sean
                                    ##### radio_in_tips = "B"
                                    # driver_daily.radio_check(radio_in_tips)
                                    if not gl.nohead:
                                        auto.prompt("等待用户手动答题...完成后请在此按回车...")
                        elif quiz_type == "weekly":
                            options = driver_weekly.radio_get_options()
                            if '因此本题选' in tips:
                                check = [x for x in letters if x in tips]
                                driver_weekly.radio_check(check)
                            else:
                                radio_in_tips, radio_out_tips = "", ""
                                '''
                                option_elements = driver_weekly.wait.until(driver_weekly.EC.presence_of_all_elements_located(
                                    (driver_weekly.By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]')))
                                # option_elements = self.find_elements(rules['challenge_options'])
                                options = [x.get_attribute("name") for x in option_elements]'''
                                for letter, option in zip(letters, options):
                                    for tip in tips:
                                        if tip in option:
                                            # print(f'{option} in tips')
                                            if letter not in radio_in_tips:
                                                radio_in_tips += letter
                                        else:
                                            # print(f'{option} out tips')
                                            if letter not in radio_out_tips:
                                                radio_out_tips += letter

                                print('含 ', radio_in_tips,
                                      '不含', radio_out_tips)
                                # and radio_in_tips not in driver_weekly.excludes:
                                if 1 == len(radio_in_tips):
                                    print('根据提示', radio_in_tips)
                                    driver_weekly.radio_check(radio_in_tips)
                                # and radio_out_tips not in excludes
                                elif 1 == len(radio_out_tips):
                                    print('根据提示', radio_out_tips)
                                    driver_weekly.radio_check(radio_out_tips)
                                # return driver_weekly._search(content, options, excludes)
                                else:
                                    max_count += 1
                                    answer_from_db = True
                                    print('无法根据提示判断，将在数据库中查询答案……')
                                    # print('将使用默认选 B')     #by Sean
                                    ##### radio_in_tips = "B"
                                    # driver_weekly.radio_check(radio_in_tips)
                                    if not gl.nohead:
                                        auto.prompt("等待用户手动答题...完成后请在此按回车...")
                        elif quiz_type == "zhuanxiang":
                            options = driver_zhuanxiang.radio_get_options()
                            if '因此本题选' in tips:
                                check = [x for x in letters if x in tips]
                                driver_zhuanxiang.radio_check(check)
                            else:
                                radio_in_tips, radio_out_tips = "", ""
                                '''
                                option_elements = driver_zhuanxiang.wait.until(driver_zhuanxiang.EC.presence_of_all_elements_located(
                                    (driver_zhuanxiang.By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]')))
                                # option_elements = self.find_elements(rules['challenge_options'])
                                options = [x.get_attribute("name") for x in option_elements]'''
                                for letter, option in zip(letters, options):
                                    for tip in tips:
                                        if tip in option:
                                            # print(f'{option} in tips')
                                            if letter not in radio_in_tips:
                                                radio_in_tips += letter
                                        else:
                                            # print(f'{option} out tips')
                                            if letter not in radio_out_tips:
                                                radio_out_tips += letter

                                print('含 ', radio_in_tips,
                                      '不含', radio_out_tips)
                                # and radio_in_tips not in driver_zhuanxiang.excludes:
                                if 1 == len(radio_in_tips):
                                    print('根据提示', radio_in_tips)
                                    driver_zhuanxiang.radio_check(
                                        radio_in_tips)
                                # and radio_out_tips not in excludes
                                elif 1 == len(radio_out_tips):
                                    print('根据提示', radio_out_tips)
                                    driver_zhuanxiang.radio_check(
                                        radio_out_tips)
                                # return driver_zhuanxiang._search(content, options, excludes)
                                else:
                                    max_count += 1
                                    answer_from_db = True
                                    print('无法根据提示判断，将在数据库中查询答案……')
                                    # print('将使用默认选 B')     #by Sean
                                    ##### radio_in_tips = "B"
                                    # driver_zhuanxiang.radio_check(radio_in_tips)
                                    if not gl.nohead:
                                        auto.prompt("等待用户手动答题...完成后请在此按回车...")
                    else:
                        print("题目类型非法")
                        if quiz_type == "daily":
                            log_daily("！！！！！有提示，但题目类型非法！！！！！")
                        break
                    time.sleep(1)
            total, scores = show_score(cookies)
            # 答题完成，并存在全局错题，进行推送
            if gl.nohead and answer_error_collect and gl.push_msg:
                gl.pushprint('')
            if scores[quiz_type] >= score_all:
                print("检测到"+quiz_zh_CN[quiz_type]+"答题分数已满,退出学 xi ")
            else:
                print(
                    "！！！！！没拿到满分，请收集日志反馈错误题目！！！！！https://github.com/TechXueXi/techxuexi-tiku/issues/1")
                auto.prompt("完成后（或懒得弄）请在此按回车...")
                # log_daily("！！！！！没拿到满分！！！！！")
        if driver_default == None:
            try:
                driver_ans.quit()
            except Exception as e:
                print('driver_ans 在 answer_question 退出时出了一点小问题...')
        else:
            pass  # 其他函数传入函数的driver，不自动退出
    else:
        print(quiz_zh_CN[quiz_type]+"答题已满分.")


def daily(cookies, scores, driver_default=None):
    quiz_type = "daily"
    score_all = const.daily_all
    quiz_xpath = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div'
    category_xpath = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]'
    answer_question(quiz_type, cookies, scores, score_all,
                    quiz_xpath, category_xpath, driver_default=driver_default)


def weekly(cookies, scores, driver_default=None):
    quiz_type = "weekly"
    score_all = const.weekly_all
    quiz_xpath = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div'
    category_xpath = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]'
    answer_question(quiz_type, cookies, scores, score_all,
                    quiz_xpath, category_xpath, driver_default=driver_default)


def zhuanxiang(cookies, scores, driver_default=None):
    quiz_type = "zhuanxiang"
    score_all = const.zhuanxiang_all
    quiz_xpath = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div'
    category_xpath = '//*[@id="app"]/div/div[2]/div/div[6]/div[1]/div[1]'
    answer_question(quiz_type, cookies, scores, score_all,
                    quiz_xpath, category_xpath, driver_default=driver_default)
