import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import apihelper
import os
import pandalearning as pdl
from pdlearn.exp_catch import exception_catcher
from pdlearn.config import cfg_get, get_env_or_cfg
import gc #资源回收

pushmode = get_env_or_cfg("addition.Pushmode", "Pushmode", "0")
token = get_env_or_cfg("addition.telegram.bot_token", "AccessToken", "")
master = get_env_or_cfg("addition.telegram.user_id", "Secret", "")
bot = telebot.TeleBot(token)


def authorize(self):
    """
    验证消息人，防止个人信息泄露
    """
    return str(self.from_user.id) == master


@bot.message_handler(commands=['start'], func=authorize)
def send_welcome(message):
    bot.reply_to(message, "一起来学xi吧！\n输入 /help 获取帮助。")


@bot.message_handler(commands=['help'], func=authorize)
def get_help(message):
    bot.reply_to(message,
                 "/help 获取帮助\n" +
                 "/learn 开始学习, /learn 张三 指定账号学习\n" +
                 "/list 获取账号列表\n" +
                 "/add 添加新账号\n" +
                 "/update 更新代码\n")


@bot.message_handler(commands=['learn'], func=authorize)
@exception_catcher(reserve_fun=bot.reply_to, fun_args=("学习崩溃啦",), args_push=True)
def learn(message):
    params = message.text.split(" ")
    if len(params) > 1:
        pdl.start(params[1] if params[1] else None)
    else:
        names = pdl.get_all_user_name()
        if len(names) <= 1:
            pdl.start(None)
        else:
            markup = InlineKeyboardMarkup()
            boards = []
            for name in names:
                boards.append(InlineKeyboardButton(name, callback_data=name))
            boards.append(InlineKeyboardButton("全部", callback_data="ALLUSER"))
            markup.add(*boards)
            bot.send_message(message.chat.id, "请选择开始学xi的账号：",
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "开始学习")
    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == "ALLUSER":
        bot.send_message(call.message.chat.id, "全部账号开始学习")
        pdl.start(None)
    else:
        bot.send_message(call.message.chat.id, call.data+" 开始学习")
        pdl.start(call.data)


@bot.message_handler(commands=['list'], func=authorize)
@exception_catcher(reserve_fun=bot.reply_to, fun_args=("Chrome 崩溃啦",), args_push=True)
def list(message):
    bot.send_chat_action(master, "typing")
    msg = pdl.get_user_list()
    bot.reply_to(message, msg)


@bot.message_handler(commands=['add'], func=authorize)
@exception_catcher(reserve_fun=bot.reply_to, fun_args=("Chrome 崩溃啦",), args_push=True)
def add(message):
    bot.send_chat_action(master, "typing")
    pdl.add_user()


@bot.message_handler(commands=['update'], func=authorize)
def rep_update(message):
    try:
        shell = "git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche "
        params = message.text.split(" ")
        if len(params) > 1:
            shell += params[1]
        msg = os.popen(shell).readlines()[-1]
        if "up to date" in msg:
            bot.send_message(message.chat.id, "当前代码已经是最新的了")
        else:
            os.popen("cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi")
            bot.send_message(message.chat.id, "代码更新完成"+msg)
    except Exception as e:
        bot.send_message(message.chat.id, "更新失败："+str(e))


@bot.message_handler(commands=['v'], func=authorize)
def rep_update(message):
    bot.reply_to(message, "当前版本：v0.10.29")


def polling():
    try:
        bot.polling(non_stop=True, timeout=120)
    except Exception as e:
        print("telegtram listener reconnecting...")
    finally: #资源回收
        gc.collect() #资源回收
        polling()


if __name__ == '__main__':
    if os.getenv('Nohead') == "True" and pushmode == "5":
        proxy = cfg_get("addition.telegram.proxy")
        if proxy and cfg_get("addition.telegram.use_proxy", False):
            apihelper.proxy = {'http': proxy, 'https': proxy}
            apihelper.CONNECT_TIMEOUT = 120
            try:
                info = bot.get_me()  # 尝试通过代理获取信息
                info.full_name
            except Exception as e:
                apihelper.proxy = {}
                print("代理请求异常，已关闭代理:"+str(e))
        bot.send_message(master, "学xi助手上线啦，快来学xi吧")
        polling()
