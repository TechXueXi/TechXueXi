import telebot
import os
import pandalearning as pdl

bot=telebot.TeleBot(os.getenv('AccessToken'))
master=os.getenv('Secret')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "一起来学xi吧！\n输入 /help 获取帮助。")

@bot.message_handler(commands=['help'])
def get_help(message):
    bot.reply_to(message,
    "/help 获取帮助\n"+
    "/learn 开始学习\n"+
    "/list 获取账号列表\n"+
    "/add 添加新账号\n")

@bot.message_handler(commands=['learn'])
def learn(message):
    try:
        pdl.start()
    except:
        bot.reply_to(message,"学习崩溃啦")

@bot.message_handler(commands=['list'])
def list(message):
    try:
        msg=pdl.get_user_list()
        bot.reply_to(message,msg)
    except:
        bot.reply_to(message,"网络异常")

@bot.message_handler(commands=['add'])
def add(message):
    try:
        pdl.add_user()
    except:
        bot.reply_to(message,"chrome 崩啦")

if __name__ == '__main__':
    if os.getenv('Nohead') == "True" and os.getenv('Pushmode')=="5":
        bot.send_message(master,"学xi助手上线啦，快来学xi吧")
        bot.polling()