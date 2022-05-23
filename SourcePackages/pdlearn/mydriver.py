import base64  # 解码二维码图片
import io
import os
import random
import re
import string
import time
import uuid
from typing import Any, List
from urllib.parse import quote, quote_plus

import lxml
import qrcode
import requests
import selenium
from bs4 import BeautifulSoup
from PIL import Image
from pyzbar import pyzbar
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pdlearn.globalvar import web
from webServerConf import WebMessage, WebQrUrl, web_db

from pdlearn import globalvar as gl, auto
from pdlearn import user, user_agent
from pdlearn.web import WebHandler
from pdlearn.config import cfg_get
from pdlearn.dingding import DingDingHandler


# from pdlearn.qywx import WeChat  # 使用微信发送二维码图片到手机


def decode_img(data):
    if None == data:
        raise Exception('未获取到二维码,请检查网络并重试')

    img_b64decode = base64.b64decode(data[data.index(';base64,') + 8:])
    decoded = pyzbar.decode(Image.open(io.BytesIO(img_b64decode)))
    return decoded[0].data.decode("utf-8")


def login(chat_id=None):
    client = requests.session()
    # 1. 获取sign
    sign: str = client.get(url="https://pc-api.xuexi.cn/open/api/sns/sign").json().get("data").get("sign")
    # 2. 获取qr
    qr_data: str = client.get("https://login.xuexi.cn/user/qrcode/generate").json().get("result")
    # 3. 生成登录链接
    code_url = f"https://login.xuexi.cn/login/qrcommit?showmenu=false&code={qr_data}&appId=dingoankubyrfkttorhpou"
    # 生成二维码
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
    qr.add_data(code_url)
    qr.make(fit=True)
    img = qr.make_image()
    img.show()
    # 二维码转base64
    output_buffer = io.BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    qrbase64 = "data:image/png;base64," + base64.b64encode(byte_data).decode("utf-8")

    # 推送消息
    if gl.nohead or cfg_get("addition.SendLoginQRcode", 0) == 1:
        print("二维码将发往机器人...\n" + "=" * 60)
        # 发送二维码
        gl.send_qrbase64(qrbase64)
        # 发送链接
        if gl.scheme:
            qrurl = gl.scheme + quote_plus(code_url)
        else:
            qrurl = decode_img(qrbase64)
        gl.pushprint(qrurl, chat_id)

    web_qr_url = ""
    web_msg = ""
    try:
        web_qr_url = web_db.session.query(
            WebQrUrl).filter_by(url=qrbase64).first()
        web_msg = web_db.session.query(
            WebMessage).filter_by(text=code_url).first()
    except Exception as e:
        print(str(e))
        print("web数据库添加失败")
        web_db.session.rollback()

    secret = ""
    print(f"sign: {sign}, data: {qr_data}")
    for i in range(60):
        resp = client.post(url="https://login.xuexi.cn/login/login_with_qr",
                           data={"qrCode": qr_data, "goto": "https://oa.xuexi.cn", "pdmToken": ""},
                           ).json()
        if resp.get("success"):
            secret = resp.get("data")
            break
        else:
            print("等待扫码中---")
        print(resp)
        time.sleep(5)
    if secret == "":
        if gl.islooplogin:
            print("循环模式开启，即将重新获取二维码")
            time.sleep(3)
            return login(chat_id)
        return None
    client.get("https://pc-api.xuexi.cn/login/secure_check",
               params={"code": secret.split("=")[1], "state": sign + str(uuid.uuid4())})

    print("token ==> " + client.cookies.get("token"))

    cookies = [{"name": "token", "value": client.cookies.get("token")}]
    user.save_cookies(cookies)
    web_qr_url and web_db.session.delete(web_qr_url)
    web_msg and web_db.session.delete(web_msg)
    web_db.session.commit()
    return cookies


class title_of_login:
    def __call__(self, driver):
        """ 用来结合webDriverWait判断出现的title """
        try:
            is_title1 = bool(EC.title_is(u'我的学习')(driver))
            is_title2 = bool(EC.title_is(u'系统维护中')(driver))
        except Exception as e:
            print("chrome 开启失败。" + str(e))
            exit()
        if is_title1 or is_title2:
            return True
        else:
            return False


class Mydriver:

    def __init__(self, noimg=True, nohead=True):
        self.web = WebHandler()
        nohead = gl.nohead
        mydriver_log = ''
        try:
            # ==================== 设置options ====================
            self.options = Options()
            if noimg:
                self.options.add_argument(
                    'blink-settings=imagesEnabled=true')  # 不加载图片, 提升速度，但无法显示二维码
            if nohead:
                self.options.add_argument('--headless')
                self.options.set_capability(
                    'unhandledPromptBehavior', 'accept')
                self.options.add_argument("--window-size=1920,1050")
            else:
                self.options.add_argument('--window-size=750,450')
                # self.options.add_argument('--window-size=400,500')
                # self.options.add_argument('--window-size=900,800')
                # self.options.add_argument("--window-size=1920,1050")

            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument(
                '--disable-software-rasterizer')  # 解决GL报错问题
            self.options.add_argument('--disable-extensions')
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--mute-audio')  # 关闭声音
            self.options.add_argument('--window-position=700,0')
            self.options.add_argument('--log-level=3')
            self.options.add_argument(
                '--user-agent={}'.format(user_agent.getheaders()))
            self.options.add_experimental_option(
                'excludeSwitches', ['enable-automation'])  # 绕过js检测
            # 在chrome79版本之后，上面的实验选项已经不能屏蔽webdriver特征了
            # 屏蔽webdriver特征
            self.options.add_argument("--disable-blink-features")
            self.options.add_argument(
                "--disable-blink-features=AutomationControlled")
            self.webdriver = webdriver

            # ==================== 寻找 chrome ====================
            if os.path.exists("./chrome/chrome.exe"):  # win
                self.options.binary_location = "./chrome/chrome.exe"
                mydriver_log = '可找到 "./chrome/chrome.exe"'
            elif os.path.exists("/opt/google/chrome/chrome"):  # linux
                self.options.binary_location = "/opt/google/chrome/chrome"
                mydriver_log = '可找到 "/opt/google/chrome/chrome"'
            # ==================== 寻找 chromedriver ====================
            chromedriver_paths = [
                "./chrome/chromedriver.exe",  # win
                "./chromedriver",  # linux
                "/usr/bin/chromedriver",  # linux用户安装
                # raspberry linux （需要包安装chromedriver）
                "/usr/lib64/chromium-browser/chromedriver",
                # raspberry linux （需要包安装chromedriver）
                "/usr/lib/chromium-browser/chromedriver",
                "/usr/local/bin/chromedriver",  # linux 包安装chromedriver
            ]
            have_find = False
            for one_path in chromedriver_paths:
                if os.path.exists(one_path):
                    self.driver = self.webdriver.Chrome(
                        executable_path=one_path, chrome_options=self.options)
                    mydriver_log = mydriver_log + '\r\n可找到 "' + one_path + '"'
                    have_find = True
                    break
            if not have_find:
                self.driver = self.webdriver.Chrome(
                    chrome_options=self.options)
                mydriver_log = mydriver_log + '\r\n未找到chromedriver，使用默认方法。'
        except:
            print("=" * 60)
            print(" Chrome 浏览器初始化失败。信息：")
            print(mydriver_log)
            print('您可以检查下：')
            print("1. 是否存在./chrome/chromedriver.exe 或 PATH 中是否存在 chromedriver.exe")
            print(
                "2. 浏览器地址栏输入 chrome://version 看到的chrome版本 和 运行 chromedriver.exe 显示的版本整数部分是否相同")
            print("针对上述问题，请在 https://registry.npmmirror.com/binary.html?path=chromedriver/ 下载对应版本程序并放在合适的位置")
            print("3. 如不是以上问题，请提issue，附上报错信息和您的环境信息")
            print("=" * 60)
            auto.prompt("按回车键继续......")
            raise

    def get_cookie_from_network(self, chat_id=None):
        print("正在打开二维码登陆界面,请稍后")
        self.web_log('正在打开二维码登陆界面,请稍后')
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
            # 修改了适配新版本的二维码的滚动位置
            self.driver.execute_script(
                'window.scrollTo(document.body.scrollWidth/2 - 200 , 400)')
        qrurl = ''
        qcbase64 = ''
        # 取出iframe中二维码，并发往钉钉
        if gl.nohead == True or cfg_get("addition.SendLoginQRcode", 0) == 1:
            print("二维码将发往机器人...\n" + "=" * 60)
            qrurl, qcbase64 = self.sendmsg(chat_id)

        # 扫码登录后删除二维码和登录链接 准备
        web_qr_url = web_db.session.query(
            WebQrUrl).filter_by(url=qcbase64).first()
        web_msg = web_db.session.query(
            WebMessage).filter_by(text=qrurl).first()

        # print(' ----------------------------------------------------------------')
        # print(web_qr_url)
        # print(' ----------------------------------------------------------------')
        # print(web_msg)
        # print(web_db.session.query(WebMessage).all())

        # try:
        #     # 取出iframe中二维码，并发往方糖，拿到的base64没办法直接发钉钉，所以发方糖
        #     if  gl.nohead==True or cfg["addition"]["SendLoginQRcode"] == 1 :
        #         print("二维码将发往方糖机器人...\n" + "=" * 60)
        #         self.toFangTang()
        # except Exception as e:
        #     print("未检测到SendLoginQRcode配置，请手动扫描二维码登陆..."+e)

        try:
            # 获取二维码图片  # 这一块等待测试完毕再加入代码
            # self.driver.switch_to.frame("ddlogin-iframe")
            # source = self.driver.page_source
            # picc = re.search(
            #     "(data:image/png;base64,)(.*)(\"></div><div data-v-be4de7b6)", source).group(2)
            # pic = base64.b64decode(picc)
            # 微信发送图片到手机，以便扫码（此配置项暂未应用至代码。结合 default_template.conf 修改）
            # wx = WeChat()
            # media_id = wx.get_media_url(pic)
            # wx.send_image(media_id)

            # WebDriverWait(self.driver, 270).until(EC.title_is(u"我的学习"))
            WebDriverWait(self.driver, 270).until(title_of_login())
            cookies = self.get_cookies()
            user.save_cookies(cookies)
            # 扫码登录后删除二维码和登录链接
            # print('扫码登录后删除二维码和登录链接 {} - {}'.format(web_msg, web_qr_url))
            self.web_log('扫码登录后删除二维码和登录链接')
            web_qr_url and web_db.session.delete(web_qr_url)
            web_msg and web_db.session.delete(web_msg)
            web_db.session.commit()
            return cookies

        except Exception as e:
            print("扫描二维码超时... 错误信息：" + str(e))
            self.web_log("扫描二维码超时... 错误信息：" + str(e))
            if (gl.islooplogin == True):
                print("循环模式开启，即将重新获取二维码")
                self.web_log("循环模式开启，即将重新获取二维码")
                time.sleep(3)
                return self.get_cookie_from_network()
            self.quit()

            if str(e).find("check_hostname") > -1 and str(e).find("server_hostname") > -1:
                print("针对“check_hostname requires server_hostname”问题：")
                print("您的网络连接存在问题，请检查您与xuexi.cn的网络连接并关闭“某些”软件")
                self.web_log(
                    "针对“check_hostname requires server_hostname”问题：")
                self.web_log(
                    "您的网络连接存在问题，请检查您与xuexi.cn的网络连接并关闭“某些”软件")
            auto.prompt("按回车键退出程序. ")
            exit()

    def web_log(self, send_log):
        self.web.add_message(send_log)

    def sendmsg(self, chat_id=None):
        qcbase64 = self.getQRcode()
        # 发送二维码
        gl.send_qrbase64(qcbase64)
        # 发送链接
        qrurl = ''
        if gl.scheme:
            qrurl = gl.scheme + quote_plus(decode_img(qcbase64))
        else:
            qrurl = decode_img(qcbase64)
        gl.pushprint(qrurl, chat_id)
        return qrurl, qcbase64

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

    def login(self, chat_id=None):
        # 调用前要先尝试从cookie加载，失败再login
        cookie_list = self.get_cookie_from_network(chat_id)
        return cookie_list

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies

    def set_cookies(self, cookies):
        try:
            # 解决Chrome 90版本无法运行的问题[https://github.com/TechXueXi/TechXueXi/issues/78]
            for cookie in cookies:
                cookie_domain = cookie["domain"]
                # fix cookie domain `.pc.xuexi.cn` caused refresh fail
                if cookie_domain.endswith("pc.xuexi.cn"):
                    self.driver.get("https://pc.xuexi.cn/")
                elif cookie_domain.endswith(".xuexi.cn"):
                    self.driver.get("https://www.xuexi.cn/")
                else:
                    print(f"unknown cookie domain {cookie_domain}, skip it")
                    continue

                # print(f'current cookie: {cookie}')
                # for expiry error (maybe old version compatibility) add by Sean 20210706
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        except exceptions.InvalidCookieDomainException as e:
            print(e.__str__)

    def title_is(self, title):
        return self.driver.title == title

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
            WebDriverWait(driver=self.driver, timeout=15,
                          poll_frequency=1).until(self.condition)
        except Exception as e:
            print('一点小问题：', e)
        self.driver.find_element_by_xpath(xpath).click()

    def xpath_getText(self, xpath):
        self.condition = EC.visibility_of_element_located(
            (By.XPATH, xpath))
        WebDriverWait(driver=self.driver, timeout=15,
                      poll_frequency=1).until(self.condition)
        return self.driver.find_element_by_xpath(xpath).text

    def check_delay(self):
        delay_time = random.randint(2, 5)
        print('等待 ', delay_time, ' 秒')
        time.sleep(delay_time)

    def _view_tips(self):  # by Sean
        # global answer
        content = ""
        try:
            # tips_open = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
            tips_open = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/span[contains(text(), "查看提示")]')
            # tips_open = self.driver.find_element_by_xpath("//span[@class='tips']")
            tips_open.click()
            print("有可点击的【查看提示】按钮")
        except Exception as e:
            print("没有可点击的【查看提示】按钮")
            try:
                answer_list = self.driver.find_element_by_css_selector(
                    ".answer").text[5:].split(' ')
                ans_options = self.radio_get_options()
                answer: List[str] = []
                for opt in ans_options:
                    for ans in answer_list:
                        if ans == opt[0]:
                            answer.append(opt)
                print("找到答案解析：", answer)

                return answer, ""
            except:
                return [], ""
        time.sleep(1)
        try:
            # tips_open = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
            tips_open = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/span[contains(text(), "查看提示")]')
            # tips_open = self.driver.find_element_by_xpath("//span[@class='tips']")
            tips_open.click()
        except Exception as e:
            print("关闭查看提示失败！没有可点击的【查看提示】按钮")
            return [], ""
        time.sleep(1)
        tip_div = self.driver.find_element_by_css_selector(
            ".ant-popover .line-feed")
        tip_full_text = tip_div.get_attribute('innerHTML')
        html = tip_full_text
        html = re.sub('</font[a-zA-Z]*?><font+.*?>',
                      '', html)  # 连续的两个font合并为一个font
        soup1 = BeautifulSoup(html, 'lxml')
        # tips.get_attribute("name") ,attrs={'color'}
        content = soup1.find_all('font')
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
            return [], ""
        time.sleep(1)
        try:
            display_tip = 0  # 页面上没有加载提示的内容
            display_tip = self.driver.find_element_by_css_selector(
                ".ant-popover-hidden")  # 关闭tip则为hidden
            if (display_tip == 0):  # 没有关闭tip
                tips_close = self.driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]')
                tips_close.click()
        except Exception as e:
            print("没有可点击的【关闭提示】按钮")
        time.sleep(1)
        return answer, tip_full_text

    def radio_get_options(self):
        html = self.driver.page_source
        soup1 = BeautifulSoup(html, 'lxml')
        content = soup1.find_all('div', attrs={'class': 'choosable'})
        if len(content) <= 0:
            content = soup1.find_all('div', attrs={'class': 'q-answer'})
        options = []
        for i in content:
            options.append(i.text)
        print('获取选项：', options)
        return options

    def radio_check(self, check_options):
        opts = self.driver.find_elements_by_class_name("choosable")
        for check_option in check_options:
            try:
                # self.driver.find_element_by_xpath(
                #     '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/div[contains(text(), "' + check_option + '.")]').click()
                for opt in opts:
                    if opt.text[0] == check_option:
                        opt.click()
            except Exception as e:
                print("点击", check_option, '失败！')
        self.check_delay()
        submit = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_class_name("action-row").find_elements_by_xpath("button"))
        if len(submit) > 1:
            self.click_xpath(
                '//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]')
            print("成功点击交卷！")
        else:
            self.click_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/button')
            print("点击进入下一题")
        time.sleep(1)
        if self.driver.find_elements_by_class_name("nc-mask-display"):
            # self.swiper_valid()
            # print("出现滑块验证。")
            gl.pushprint("出现滑块验证，本次答题结束")
            raise Exception("出现滑块验证。")

    # 滑块验证
    def swiper_valid(self):
        builder = ActionChains(self.driver)
        builder.reset_actions()
        track = self.move_mouse(300)
        builder.move_to_element(
            self.driver.find_element_by_class_name("btn_slide"))
        builder.click_and_hold()
        time.sleep(0.2)
        for i in track:
            builder.move_by_offset(xoffset=i, yoffset=0)
            builder.reset_actions()
        time.sleep(0.1)
        # 释放左键，执行for中的操作
        builder.release().perform()
        time.sleep(5)
        self.swiper_valid()

    # 鼠标移动

    def move_mouse(self, distance):
        remaining_dist = distance
        moves = []
        a = 0
        # 加速度，速度越来越快...
        while remaining_dist > 0:
            span = random.randint(15, 20)
            a += span
            moves.append(a)
            remaining_dist -= span
            if sum(moves[:-1]) > 300:
                print(sum(moves))
                break
        return moves

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

    def fill_in_blank(self, answer):  # by Sean
        # ans = WebDriverWait(self.driver, 15).until(
        #     lambda driver: driver.find_elements_by_xpath("//input[@type='text']"))
        # #去除answer中的空格
        # for i in range(len(answer)):
        #     if (answer[i] == ''):
        #         del answer[i]
        # #无答案题
        # if (answer == ['好']):
        #     print('可能是视频题')
        #     for i in range(0, len(ans)):
        #         try:
        #             ans[i].send_keys(answer)
        #         except Exception as e:
        #             print(e)
        #             pass
        #         continue
        # #答案数量不一致题
        # elif (len(ans)!=len(answer)):
        #     print ('答案数量不对')
        #     answer = ['好']
        #     for i in range(0, len(ans)):
        #         try:
        #             ans[i].send_keys(answer)
        #         except Exception as e:
        #             print(e)
        #             pass
        #         continue
        # else:
        #     for i in range(0, len(answer)):
        #         try:
        #             self.driver.find_element_by_xpath(
        #                 '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[2]/div/input[' + str(i + 1) + ']').send_keys(answer[i])
        #             # self.driver.find_element_by_xpath("//input[" + str(i + 1) + "]").send_keys(answer[i])
        #         except Exception as e:
        #             print(e)
        #             try:
        #                 ans[i].send_keys(answer[i])
        #             except Exception as e:
        #                 print(e)
        #                 pass
        #             pass
        #             # print('可能是视频题')
        #             # self.driver.find_element_by_xpath("//input[@type='text']").send_keys(answer[i])
        #             # self.driver.find_element_by_xpath(
        #             #    '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/div/input[' + str(i + 1) + ']').send_keys(answer[i])
        #         continue
        for i in range(0, len(answer)):
            try:
                input = self.driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[2]/div/input[' + str(i + 1) + ']')
            except:  # 视频题，多一个div
                input = self.driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/div/input[' + str(i + 1) + ']')
            input.send_keys(answer[i])
        self.check_delay()
        submit = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_class_name("action-row").find_elements_by_xpath("button"))
        if len(submit) > 1:
            self.click_xpath(
                '//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]')
            print("成功点击交卷！")
        else:
            self.click_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/button')
            print("点击进入下一题")

    def zhuanxiang_fill_in_blank(self, answer):
        for i in range(0, len(answer)):
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div/div[6]/div[1]/div[2]/div/input[' + str(i + 1) + ']').send_keys(answer[i])
        self.check_delay()
        submit = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_class_name("action-row").find_elements_by_xpath("button"))
        if len(submit) > 1:
            self.click_xpath(
                '//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]')
            print("成功点击交卷！")
        else:
            self.click_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/button')
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
        url = quote("https://www.sogou.com/web?query=" +
                    content, safe=string.printable)
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
