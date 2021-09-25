import telebot
import os
from pdlearn import threads
bot=telebot.TeleBot(os.getenv('AccessToken'), parse_mode=None)
master=os.getenv('Secret')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "一起来学xi吧")

def send_message(message):
    bot.send_message(master, message)

def send_qrurl(url):
    bot.send_photo(master,url)
# 监听消息
#bot.polling