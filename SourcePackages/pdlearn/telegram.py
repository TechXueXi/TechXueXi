import telebot
from telebot import apihelper
from pdlearn.config import cfg_get


class TelegarmHandler:
    def __init__(self, token, secret, proxy=None):
        self.bot = telebot.TeleBot(token)
        self.master = secret
        if proxy and cfg_get("addition.telegram.use_proxy", False):
            apihelper.proxy = {'http': proxy, 'https': proxy}
            try:
                info = self.bot.get_me()  # 尝试通过代理获取西信息
                info.full_name
            except Exception as e:
                apihelper.proxy = {}
                print("代理请求异常，已关闭代理:"+str(e))

    def send_message(self, message):
        self.bot.send_message(self.master, message)

    def send_qrurl(self, url):
        self.bot.send_photo(self.master, url)
