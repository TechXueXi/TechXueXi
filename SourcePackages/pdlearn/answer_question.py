import time
import random
from pdlearn import user
from pdlearn import color
from pdlearn.mydriver import Mydriver
from pdlearn.score import show_score
from pdlearn.const import const
from pdlearn.log import *


def check_delay():
    delay_time = random.randint(2, 5)
    print('等待 ', delay_time, ' 秒')
    time.sleep(delay_time)



def find_available_quiz(quiz_type, driver_ans, uid):
    pages = driver_ans.driver.find_elements_by_css_selector(".ant-pagination-item")
    for p in range(len(pages)-1, -1, -1):  # 从最后一页开始往前找做题
        time.sleep(0.5)
        print('进入答题第' + str(p+1) + '页')
        pages[p].click()
        time.sleep(0.5)
        if quiz_type == "weekly":  # 寻找可以做的题
            dati = driver_ans.driver.find_elements_by_css_selector("#app .month .week button")
        elif quiz_type == "zhuanxiang":  # 寻找可以做的题
            # 可以使用 #app .items .item button:not(.ant-btn-background-ghost) 选择器，但会遗漏掉”继续答题“的部分
            dati = driver_ans.driver.find_elements_by_css_selector("#app .items .item button")
        for i in range(len(dati)-1, -1, -1):  # 从最后一个遍历到第一个
            j = dati[i]
            if ("重新" in j.text or "满分" in j.text):
                continue
            else:
                to_click = j
                # input("wait for Enter press...")
                return to_click


def answer_question(quiz_type, cookies, scores, score_all, quiz_xpath, category_xpath, uid=None, driver_default=None):
    quiz_zh_CN={"daily": "每日", "weekly": "每周", "zhuanxiang": "专项"}
    if(quiz_type not in ["daily", "weekly", "zhuanxiang"]):
        print("quiz_type 错误。收到的quiz_type："+quiz_type)
        exit(0)
    if uid is None:
        uid = user.get_userId(cookies)
    if scores[quiz_type] < score_all:  # 还没有满分，需要答题
        if driver_default is None:
            driver_ans = Mydriver(nohead=True)
        else:
            driver_ans = driver_default

        driver_daily = driver_ans
        driver_weekly = driver_ans
        driver_zhuanxiang = driver_ans
        driver_ans.driver.maximize_window()

        print('请保持窗口最大化\n'*3)
        driver_ans.get_url("https://www.xuexi.cn/notFound.html")
        driver_ans.set_cookies(cookies)
        try_count = 0
        if scores[quiz_type] < score_all:
            letters = list("ABCDEFGHIJKLMN")
            driver_ans.get_url('https://pc.xuexi.cn/points/my-points.html')

            driver_ans.click_xpath(quiz_xpath)  # 点击各个题目的去答题按钮
            time.sleep(2)
            if quiz_type != "daily":  # 如果是每日答题就不用找available了
                to_click = find_available_quiz(quiz_type, driver_ans, uid)
                if to_click is not None:
                    to_click.click()
                    time.sleep(0.5)
                else:
                    print(color.blue("无题可答。即将跳过。"))
                    if driver_default == None:
                        try:
                            driver_ans.quit()
                        except Exception as e:
                            print('driver_ans 在 answer_question 退出时出了一点小问题...')
                    else:
                        pass #其他函数传入函数的driver，不自动退出

            while scores[quiz_type] < score_all:
                if quiz_type == "weekly":
                    '''# 
                    # =======
                    #            flag = 1
                    #            page_num = 1
                    #            last_page = int(driver_weekly.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[5]/ul/li[last()-1]/a').text)
                    #            while page_num < last_page and flag == 1:
                    #                print('进入每周答题第'+ str(page_num) +'页')
                    #                all_month = len(driver_weekly.driver.find_elements_by_class_name('month'))
                    #                cur_month = 1
                    #                for tem in range(0, all_month):
                    #                    for tem2 in range(0, 6):
                    #                        if flag == 0:
                    #                            break
                    #                        try:
                    #                            temword = driver_weekly.driver.find_element_by_xpath(
                    #                                '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                    #                                    tem2 + 1) + ']/button').text
                    #                        except:
                    #                            temword = ''
                    #                            if all_month == cur_month:
                    #                                driver_weekly.click_xpath(
                    #                                        '//*[@id="app"]/div/div[2]/div/div[5]/ul/li[' + str(page_num + 2) + ']')
                    #                                print('切换至下一页')
                    #                                page_num += 1
                    #                                time.sleep(2)
                    #                            cur_month += 1
                    #                            break
                    #                        name_list = ["开始答题", "继续答题"]
                    #                        if flag == 1 and (any(name in temword for name in name_list)):
                    #                            driver_weekly.click_xpath(
                    #                                '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                    #                                    tem2 + 1) + ']/button')
                    #                            flag = 0
                    #                        elif '重新答题' in temword:
                    #                            continue
                    #            while each[6] < 5 and try_count < 10:
                    # >>>>>>> dev
                    # '''
                try:
                    category = driver_ans.xpath_getText( #获取题目类型
                    category_xpath )  # get_attribute("name")
                except Exception as e:
                    print('查找题目类型...查找元素失败！')
                    break
                print(category)
                if quiz_type == "daily":
                    ans_results = driver_ans.driver.find_elements_by_css_selector(".practice-result .infos .info")
                    if(len(ans_results) != 0): #已经找到答题结果页面
                        print(ans_results[0].get_attribute("innerHTML"))
                        print(ans_results[0].text)
                        print(ans_results[2].get_attribute("innerHTML"))
                        print(ans_results[2].text)

                        time.sleep(3)
                        # exit(2)
                        break

                    log_daily("\n====================")
                    log_daily(log_timestamp())
                    log_daily("【"+category+"】")
                    log_daily("【题干】")
                    q_body = driver_ans.driver.find_element_by_css_selector(".q-body")
                    q_html = q_body.get_attribute('innerHTML')
                    q_text = q_body.text
                    print(q_text)
                    log_daily(q_html)
                tips, tip_full_text = driver_ans._view_tips()
                if quiz_type == "daily":
                    log_daily("【提示信息】")
                    log_daily(str(tips)+"\n"+tip_full_text)
                if not tips:
                    print("本题没有提示")
                    #if quiz_type == "daily":
                    #    log_daily("！！！！！本题没有找到提示，暂时略过！！！！！")

                    #    input("等待用户手动答题...完成后请在此按回车...")
                    #    time.sleep(3)

                    if "填空题" in category:
                        print('没有找到提示，暂时略过')
                        print('使用默认答案  好 ')   #如无填空答案，使用默认答案 好 字 by Sean
                        tips = ['好']
                        #continue
                    elif "多选题" in category:
                        print('没有找到提示，暂时略过')
                        print('使用默认答案 全选')    #by Sean
                        #continue
                    elif "单选题" in category:
                        print('没有找到提示，暂时略过') #如无单选答案，使用默认答案
                        print('使用默认答案 B')   #by Sean
                        #continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        if quiz_type == "daily":
                            log_daily("！！！！！无提示，题目类型非法！！！！！")
                        break
                if "填空题" in category:
                    answer = tips
                    if quiz_type != "zhuanxiang":
                        driver_ans.fill_in_blank(answer)
                    else:#两个函数是一样的，合并为一个
                        driver_ans.fill_in_blank(answer)
                elif "多选题" in category:
                    if quiz_type == "daily":
                        options = driver_daily.radio_get_options()
                        len_option = len(options)
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

                        print('包含提示的选项 ', radio_in_tips, '，不包含提示的选项 ', radio_out_tips)
                        log_daily('包含提示的选项 '+str(radio_in_tips)+'，不包含提示的选项 '+str(radio_out_tips))
                        if len(radio_in_tips) > 1:  # and radio_in_tips not in driver_daily.excludes:
                            print('根据提示', radio_in_tips)
                            driver_daily.radio_check(radio_in_tips)
                        elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_daily.radio_check(radio_out_tips)
                        # return driver_daily._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，请自行答题……')
                            #log_daily("！！！！！无法根据提示判断，请自行答题……！！！！！")
                            print('将使用默认全选答题')     #by Sean
                            len_option = len(options)
                            radio_in_tips = letters[:len_option]
                            driver_daily.radio_check(radio_in_tips)
                            #input("等待用户手动答题...完成后请在此按回车...")

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
                        if len(radio_in_tips) > 1:  # and radio_in_tips not in driver_weekly.excludes:
                            print('根据提示', radio_in_tips)
                            driver_weekly.radio_check(radio_in_tips)
                        elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_weekly.radio_check(radio_out_tips)
                        # return driver_weekly._search(content, options, excludes)
                        else:

                            print('无法根据提示判断，请自行准备搜索……')
                            print('将使用默认全选答题')     #by Sean
                            len_option = len(options)
                            radio_in_tips = letters[:len_option]
                            driver_weekly.radio_check(radio_in_tips)
                            #input("等待用户手动答题...完成后请在此按回车...")

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
                        if len(radio_in_tips) > 1:  # and radio_in_tips not in driver_zhuanxiang.excludes:
                            print('根据提示', radio_in_tips)
                            driver_zhuanxiang.radio_check(radio_in_tips)
                        elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_zhuanxiang.radio_check(radio_out_tips)
                        # return driver_zhuanxiang._search(content, options, excludes)
                        else:

                            print('无法根据提示判断，请自行准备搜索……')
                            print('将使用默认全选答题')     #by Sean
                            len_option = len(options)
                            radio_in_tips = letters[:len_option]
                            driver_zhuanxiang.radio_check(radio_in_tips)
                            #input("等待用户手动答题...完成后请在此按回车...")

                elif "单选题" in category:
                    if quiz_type == "daily":
                        options = driver_daily.radio_get_options()
                        log_daily("【单选题选项】")
                        log_daily(str(options))
                        if '因此本题选' in tips: #提示类型1
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

                            print('包含提示的选项 ', radio_in_tips, '，不包含提示的选项 ', radio_out_tips)
                            log_daily('包含提示的选项 '+str(radio_in_tips)+'，不包含提示的选项 '+str(radio_out_tips))
                            if 1 == len(radio_in_tips):  # and radio_in_tips not in driver_daily.excludes:
                                print('根据提示', radio_in_tips)
                                driver_daily.radio_check(radio_in_tips)
                            elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                                print('根据提示', radio_out_tips)
                                driver_daily.radio_check(radio_out_tips)
                            # return driver_daily._search(content, options, excludes)
                            else:
                                print('无法根据提示判断，请自行答题……')
                                #log_daily("！！！！！无法根据提示判断，请自行答题……！！！！！")
                                print('将使用默认选 B')     #by Sean
                                radio_in_tips = "B"
                                driver_daily.radio_check(radio_in_tips)
                                #input("等待用户手动答题...完成后请在此按回车...")

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

                            print('含 ', radio_in_tips, '不含', radio_out_tips)
                            if 1 == len(radio_in_tips):  # and radio_in_tips not in driver_weekly.excludes:
                                print('根据提示', radio_in_tips)
                                driver_weekly.radio_check(radio_in_tips)
                            elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                                print('根据提示', radio_out_tips)
                                driver_weekly.radio_check(radio_out_tips)
                            # return driver_weekly._search(content, options, excludes)
                            else:

                                print('无法根据提示判断，请自行准备搜索……')
                                print('将使用默认选 B')     #by Sean
                                radio_in_tips = "B"
                                driver_weekly.radio_check(radio_in_tips)
                                #input("等待用户手动答题...完成后请在此按回车...")

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

                            print('含 ', radio_in_tips, '不含', radio_out_tips)
                            if 1 == len(radio_in_tips):  # and radio_in_tips not in driver_zhuanxiang.excludes:
                                print('根据提示', radio_in_tips)
                                driver_zhuanxiang.radio_check(radio_in_tips)
                            elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                                print('根据提示', radio_out_tips)
                                driver_zhuanxiang.radio_check(radio_out_tips)
                            # return driver_zhuanxiang._search(content, options, excludes)
                            else:

                                print('无法根据提示判断，请自行准备搜索……')
                                print('将使用默认选 B')     #by Sean
                                radio_in_tips = "B"
                                driver_zhuanxiang.radio_check(radio_in_tips)
                                #input("等待用户手动答题...完成后请在此按回车...")

                else:
                    print("题目类型非法")
                    if quiz_type == "daily":
                        log_daily("！！！！！有提示，但题目类型非法！！！！！")
                    break
                time.sleep(1)

            total, scores = show_score(cookies)
            if scores[quiz_type] >= score_all:
                print("检测到"+quiz_zh_CN[quiz_type]+"答题分数已满,退出学习")
            else:
                print("！！！！！没拿到满分，请收集日志反馈错误题目！！！！！")
                #input("完成后（或懒得弄）请在此按回车...")
                #log_daily("！！！！！没拿到满分！！！！！")
        if driver_default == None:
            try:
                driver_ans.quit()
            except Exception as e:
                print('driver_ans 在 answer_question 退出时出了一点小问题...')
        else:
            pass #其他函数传入函数的driver，不自动退出
    else:
        print(quiz_zh_CN[quiz_type]+"答题已满分.")



def daily(cookies, scores, driver_default=None):

    quiz_type = "daily"
    score_all = const.daily_all
    quiz_xpath = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div'
    category_xpath = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]'

    answer_question(quiz_type, cookies, scores, score_all, quiz_xpath, category_xpath, driver_default=driver_default)


def weekly(cookies, scores, driver_default=None):

    quiz_type = "weekly"
    score_all = const.weekly_all
    quiz_xpath = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div'
    category_xpath = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]'

    answer_question(quiz_type, cookies, scores, score_all, quiz_xpath, category_xpath, driver_default=driver_default)


def zhuanxiang(cookies, scores, driver_default=None):

    quiz_type = "zhuanxiang"
    score_all = const.zhuanxiang_all
    quiz_xpath = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div'
    category_xpath = '//*[@id="app"]/div/div[2]/div/div[6]/div[1]/div[1]'

    answer_question(quiz_type, cookies, scores, score_all, quiz_xpath, category_xpath, driver_default=driver_default)


