import telebot
class TelegarmHandler:
    def __init__(self, token, secret):
        self.bot = telebot.TeleBot(token)
        self.master=secret

    def send_message(self,message):
        self.bot.send_message(self.master, message)

    def send_qrurl(self,url):
        self.bot.send_photo(self.master,url)