# 是否是无界面模式，一般用在命令行，docker上
from pdlearn.pluspush import PlusPushHandler
from pdlearn.fangtang import FangtangHandler
from pdlearn.dingding import DingDingHandler
from pdlearn.telegram import TelegarmHandler
from pdlearn.wechat import WechatHandler
from pdlearn.web import WebHandler
import io
from PIL import Image
from pdlearn.config import cfg_get
import os
import base64  # 解码二维码图片

# 全局变量是否已经初始化
is_init = False
pushmode = "0"  # 0 不开启 1 钉钉 2 微信（并未实现） 3 Server 酱 4 pluspush 5 Telegram Bot 6 Web Dashboard
nohead = False
accesstoken = ""
topic = ''
secret = ""
islooplogin = False
zhuanxiang = False
scheme = ""
lock = False
stime = False
single = False
tg_bot = TelegarmHandler
wechat = WechatHandler
web = WebHandler()
push_msg = ""


def init_global():
    """
    初始化全局变量
    """
    global nohead, islooplogin, single, scheme, pushmode, accesstoken, secret, zhuanxiang, is_init, lock, stime, tg_bot, wechat, topic
    if os.getenv('Nohead') == "True":
        nohead = True
    else:
        nohead = cfg_get("addition.Nohead", False)
        
    if os.getenv('islooplogin') == "True":
        islooplogin = True

    if os.getenv('Single') == "True":
        single = True

    if os.getenv('Pushmode'):
        pushmode = os.getenv('Pushmode')
    else:
        pushmode = cfg_get("addition.Pushmode", "0")

    if os.getenv("Scheme") != None:
        scheme = os.getenv("Scheme")
    # elif pushmode in ["5"]: # telegram 默认开启我们提供的
    #    scheme = 'https://techxuexi.js.org/jump/techxuexi-20211023.html?'

    if os.getenv('AccessToken'):
        accesstoken = os.getenv('AccessToken')
    else:
        if pushmode == "5":
            accesstoken = cfg_get("addition.telegram.bot_token", "")
        else:
            accesstoken = cfg_get("addition.token", "")

    if os.getenv('Secret'):
        secret = os.getenv('Secret')
    else:
        if pushmode == "5":
            secret = str(cfg_get("addition.telegram.user_id", ""))
        else:
            secret = cfg_get("addition.secret", "")

    if os.getenv("ZhuanXiang"):
        zhuanxiang = os.getenv("ZhuanXiang") == "True"
    else:
        zhuanxiang = cfg_get("parameter.zhuanxiang_nohead", False)
    if pushmode == "5":
        tg_bot = TelegarmHandler(
            accesstoken, secret, cfg_get("addition.telegram.proxy"))
    if pushmode == "2":
        wechat = WechatHandler()

    # pushplus topic
    topic = os.getenv('topic') if os.getenv('topic') else ''
    is_init = True


def pushprint(text, chat_id=None):
    """
    推送或者显示
    """
    global push_msg
    if nohead == True:
        # 如果存在全局消息，追加该消息，同时发送，并清空该消息
        if push_msg:
            text = push_msg+"\n"+text
            push_msg = ''
        print(accesstoken, secret)
        if pushmode == "1":
            push = DingDingHandler(accesstoken, secret)
            push.ddtextsend(text)
        elif pushmode == "2":
            if chat_id:
                chat_id = wechat.get_opendid_by_uid(chat_id)
            wechat.send_text(text, uid=chat_id)
        elif pushmode == "3":
            push = FangtangHandler(accesstoken)
            push.fttext(text)
        elif pushmode == "4":
            push = PlusPushHandler(accesstoken, topic)
            push.fttext(text)
        elif pushmode == "5":
            tg_bot.send_message(text)
        elif pushmode == "6":
            web.add_message(text)
    print(text)


def send_qrbase64(qcbase64):
    """
    推送登录二维码
    """
    if pushmode == "3":
        ft = FangtangHandler(accesstoken)
        ft.ftmsgsend(qcbase64)
    elif pushmode == "4":
        push = PlusPushHandler(accesstoken, topic)
        push.ftmsgsend(qcbase64)
    elif pushmode == "5" and cfg_get("addition.telegram.send_qrimage", 0) == 1:
        img_b64decode = base64.b64decode(
            qcbase64[qcbase64.index(';base64,')+8:])
        tg_bot.send_qrurl(Image.open(io.BytesIO(img_b64decode)))
    elif pushmode == "6":
        web.add_qrurl(qcbase64)
