from typing import List, Any

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from pdlearn import user_agent
from pdlearn import user
from pdlearn.dingding import DingDingHandler
from pdlearn.config import cfg
from bs4 import BeautifulSoup
import string
import lxml
import os
import time
import requests
import random
from urllib.parse import quote
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions


def title_of_login(my_driver, title=u"我的学习"):
    """ 用来结合webDriverWait判断出现的title """
    is_title1 = bool(EC.title_is(title)(my_driver.driver))
    is_title2 = bool(EC.title_is(u'系统维护中')(my_driver.driver))
    if is_title1 or is_title2:
        return True
    else:
        return False


class Mydriver:

    def __init__(self, noimg=True, nohead=True):
        mydriver_log=''
        try:
            # ==================== 设置options ====================
            self.options = Options()
            if noimg:
                self.options.add_argument('blink-settings=imagesEnabled=true')  # 不加载图片, 提升速度，但无法显示二维码
            if nohead:
                self.options.add_argument('--headless')
                self.options.add_argument('--disable-extensions')
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--no-sandbox')
                self.options.add_argument('--disable-software-rasterizer')  # 解决GL报错问题
            self.options.add_argument('--mute-audio')  # 关闭声音
            # self.options.add_argument('--window-size=400,500')
            self.options.add_argument('--window-size=750,450')
            # self.options.add_argument('--window-size=900,800')
            self.options.add_argument('--window-position=700,0')
            self.options.add_argument('--log-level=3')
            self.options.add_argument('--user-agent={}'.format(user_agent.getheaders()))
            self.options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 绕过js检测
            # 在chrome79版本之后，上面的实验选项已经不能屏蔽webdriver特征了
            # 屏蔽webdriver特征
            self.options.add_argument("--disable-blink-features")
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            self.webdriver = webdriver
            # ==================== 寻找 chrome ====================
            if os.path.exists("./chrome/chrome.exe"):  # win
                self.options.binary_location = "./chrome/chrome.exe"
                mydriver_log='可找到 "./chrome/chrome.exe"'
            elif os.path.exists("/opt/google/chrome/chrome"):  # linux
                self.options.binary_location = "/opt/google/chrome/chrome"
                mydriver_log='可找到 "/opt/google/chrome/chrome"'
            # ==================== 寻找 chromedriver ====================
            chromedriver_paths = [
                "./chrome/chromedriver.exe",                # win
                "./chromedriver",                           # linux
                "/usr/bin/chromedriver",                    # linux用户安装
                "/usr/lib64/chromium-browser/chromedriver", # raspberry linux （需要包安装chromedriver）
                "/usr/lib/chromium-browser/chromedriver",   # raspberry linux （需要包安装chromedriver）
                "/usr/local/bin/chromedriver",              # linux 包安装chromedriver
            ]
            have_find = False
            for one_path in chromedriver_paths:
                if os.path.exists(one_path):
                    self.driver = self.webdriver.Chrome(executable_path=one_path, chrome_options=self.options)
                    mydriver_log=mydriver_log+'\r\n可找到 "' + one_path + '"'
                    have_find = True
                    break
            if not have_find:
                self.driver = self.webdriver.Chrome(chrome_options=self.options)
                mydriver_log=mydriver_log+'\r\n未找到chromedriver，使用默认方法。'
        except:
            print("=" * 60)
            print(" Chrome 浏览器初始化失败。信息：")
            print(mydriver_log)
            print('您可以检查下：')
            print("1. 是否存在./chrome/chromedriver.exe 或 PATH 中是否存在 chromedriver.exe")
            print("2. 浏览器地址栏输入 chrome://version 看到的chrome版本 和 运行 chromedriver.exe 显示的版本整数部分是否相同")
            print("针对上述问题，请在 http://npm.taobao.org/mirrors/chromedriver 下载对应版本程序并放在合适的位置")
            print("3. 如不是以上问题，请提issue，附上报错信息和您的环境信息")
            print("=" * 60)
            input("按回车键继续......")
            raise

    def get_cookie_from_network(self):
        print("正在打开二维码登陆界面,请稍后")
        self.driver.get("https://pc.xuexi.cn/points/login.html")
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("redflagbox"))
        except exceptions.TimeoutException:
            print("网络缓慢，请重试")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("layout-header"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("layout-footer"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
            self.driver.execute_script('window.scrollTo(document.body.scrollWidth/2 - 200 , 0)')


        try: 
            # 取出iframe中二维码，并发往钉钉
            if cfg["addition"]["SendLoginQRcode"] == "1":
                print("二维码将发往钉钉机器人...\n" + "=" * 60)
                self.toDingDing()
        except KeyError as e:
            print("未检测到SendLoginQRcode配置，请手动扫描二维码登陆...")


        try:
            # WebDriverWait(self.driver, 270).until(EC.title_is(u"我的学 xi "))
            WebDriverWait(self.driver, 270).until(title_of_login(self))
            cookies = self.get_cookies()
            
            user.save_cookies(cookies)
            
            return cookies
        except Exception as e:
            self.quit()
            print("扫描二维码超时... 错误信息：" + str(e))
            if str(e).find("check_hostname") > -1 and str(e).find("server_hostname") > -1:
                print("针对“check_hostname requires server_hostname”问题：")
                print("您的网络连接存在问题，请检查您与xuexi.cn的网络连接并关闭“某些”软件")
            input("按回车键退出程序. ")
            exit()

    def toDingDing(self):
        token = cfg["addition"]["token"]
        secret = cfg["addition"]["secret"]
        ddhandler = DingDingHandler(token, secret)
        ddhandler.ddmsgsend(self.getQRcode())

    def getQRcode(self):
        try:
            # 获取iframe内的二维码
            self.driver.switch_to.frame(
                WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_id("ddlogin-iframe"))
            )
            img = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_tag_name("img")
            )
            path = img.get_attribute("src")
            self.driver.switch_to.default_content()
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            return path

    def login(self):
        # 调用前要先尝试从cookie加载，失败再login
        cookie_list = self.get_cookie_from_network()
        return cookie_list

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies

    def set_cookies(self, cookies):
        try:
            # 解决Chrome 90版本无法运行的问题[https://github.com/TechXueXi/TechXueXi/issues/78]
            for cookie in cookies:
                if cookie['domain'] == 'pc.xuexi.cn':
                    self.driver.get("https://pc.xuexi.cn/")
                if cookie['domain'] == '.xuexi.cn':
                    self.driver.get("https://www.xuexi.cn/")
                # print(f'current cookie: {cookie}')
                self.driver.add_cookie(cookie)
        except exceptions.InvalidCookieDomainException as e:
            print(e.__str__)

    def get_url(self, url):
        self.driver.get(url)

    def go_js(self, js):
        self.driver.execute_script(js)

    def quit(self):
        self.driver.quit()

    def click_xpath(self, xpath):
        try:
            self.condition = EC.visibility_of_element_located(
                (By.XPATH, xpath))
            WebDriverWait(driver=self.driver, timeout=15, poll_frequency=1).until(self.condition)
        except Exception as e:
            print('一点小问题：', e)
        self.driver.find_element_by_xpath(xpath).click()

    def xpath_getText(self, xpath):
        self.condition = EC.visibility_of_element_located(
            (By.XPATH, xpath))
        WebDriverWait(driver=self.driver, timeout=15, poll_frequency=1).until(self.condition)
        return self.driver.find_element_by_xpath(xpath).text

    def check_delay(self):
        delay_time = random.randint(2, 8)
        print('等待 ', delay_time, ' 秒')
        time.sleep(delay_time)

    def _view_tips(self):
        # global answer
        content = ""
        try:
            # tips_open = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
            tips_open = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/span[contains(text(), "查看提示")]')
            tips_open.click()
            print("有可点击的【查看提示】按钮")
        except Exception as e:
            print("没有可点击的【查看提示】按钮")
            return [],""
        time.sleep(1)
        try:
            # tips_open = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
            tips_open = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/span[contains(text(), "查看提示")]')
            tips_open.click()
        except Exception as e:
            print("关闭查看提示失败！没有可点击的【查看提示】按钮")
            return [],""
        tip_div = self.driver.find_element_by_css_selector(".ant-popover .line-feed")
        tip_full_text = tip_div.get_attribute('innerHTML')
        html = tip_full_text
        html = re.sub('</font[a-zA-Z]*?><font+.*?>', '', html)  # 连续的两个font合并为一个font
        soup1 = BeautifulSoup(html, 'lxml')
        content = soup1.find_all('font')  # tips.get_attribute("name") ,attrs={'color'}
        answer: List[str] = []
        try:
            for i in content:
                answer.append(i.text)
                '''
            if len(answer) >= 2:
                answer=str.join(answer)
            if (',' or '.' or '，' or '。' or '、') in answer:
                answer=re.split(",|，|.|。|、",answer)
                '''
            print('获取提示：', answer)
        except Exception as e:
            print('无法处理提示内容，请检查日志.')
            print(e)
            return [],""
        time.sleep(1)
        try:
            display_tip = 0 #页面上没有加载提示的内容
            display_tip = self.driver.find_element_by_css_selector(".ant-popover-hidden") #关闭tip则为hidden
            if(display_tip == 0): # 没有关闭tip
                tips_close = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]')
                tips_close.click()
        except Exception as e:
            print("没有可点击的【关闭提示】按钮")
        time.sleep(1)
        return answer, tip_full_text

    def radio_get_options(self):
        html = self.driver.page_source
        soup1 = BeautifulSoup(html, 'lxml')
        content = soup1.find_all('div', attrs={'class': 'choosable'})
        options = []
        for i in content:
            options.append(i.text)
        print('获取选项：', options)
        return options

    def radio_check(self, check_options):
        for check_option in check_options:
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/div[contains(text(), "' + check_option + '")]').click()
            except Exception as e:
                print("点击", check_option, '失败！')
        self.check_delay()
        submit = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_class_name("action-row").find_elements_by_xpath("button"))
        if len(submit) > 1:
            self.click_xpath('//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]')
            print("成功点击交卷！")
        else:
            self.click_xpath('//*[@id="app"]/div/div[*]/div/div[*]/div[*]/button')
            print("点击进入下一题")

    def blank_get(self):
        html = self.driver.page_source
        soup1 = BeautifulSoup(html, 'lxml')
        content = soup1.find_all('div', attrs={'class': 'q-body'})
        print('原始', content)
        content = soup1.find('div', attrs={'class': 'q-body'}).getText()
        print(content)
        # content1=content.text
        dest = re.findall(r'.{0,2}\s+.{0,2}', content)
        print('填空反馈')
        print(dest)

    def fill_in_blank(self, answer):
        for i in range(0, len(answer)):
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[2]/div/input[' + str(i + 1) + ']').send_keys(answer[i])
        self.check_delay()
        submit = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_class_name("action-row").find_elements_by_xpath("button"))
        if len(submit) > 1:
            self.click_xpath('//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]')
            print("成功点击交卷！")
        else:
            self.click_xpath('//*[@id="app"]/div/div[*]/div/div[*]/div[*]/button')
            print("点击进入下一题")

    def zhuanxiang_fill_in_blank(self, answer):
        for i in range(0, len(answer)):
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div/div[6]/div[1]/div[2]/div/input[' + str(i + 1) + ']').send_keys(answer[i])
        self.check_delay()
        submit = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_class_name("action-row").find_elements_by_xpath("button"))
        if len(submit) > 1:
            self.click_xpath('//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]')
            print("成功点击交卷！")
        else:
            self.click_xpath('//*[@id="app"]/div/div[*]/div/div[*]/div[*]/button')
            print("点击进入下一题")

    def _search(self, content, options, exclude=''):
        # 职责 网上搜索
        print(f'搜索 {content} <exclude = {exclude}>')
        print(f"选项 {options}")
        content = re.sub(r'[\(（]出题单位.*', "", content)
        if options[-1].startswith("以上") and chr(len(options) + 64) not in exclude:
            print(f'根据经验: {chr(len(options) + 64)} 很可能是正确答案')
            return chr(len(options) + 64)
        # url = quote('https://www.baidu.com/s?wd=' + content, safe=string.printable)
        url = quote("https://www.sogou.com/web?query=" + content, safe=string.printable)
        response = requests.get(url, headers=self.headers).text
        counts = []
        for i, option in zip(['A', 'B', 'C', 'D', 'E', 'F'], options):
            count = response.count(option)
            counts.append((count, i))
            print(f'{i}. {option}: {count} 次')
        counts = sorted(counts, key=lambda x: x[0], reverse=True)
        counts = [x for x in counts if x[1] not in exclude]
        c, i = counts[0]
        if 0 == c:
            # 替换了百度引擎为搜狗引擎，结果全为零的机会应该会大幅降低       
            _, i = random.choice(counts)
            print(f'搜索结果全0，随机一个 {i}')
        print(f'根据搜索结果: {i} 很可能是正确答案')
        return i
