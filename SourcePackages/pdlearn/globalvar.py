# 是否是无界面模式，一般用在命令行，docker上
from pdlearn.pluspush import PlusPushHandler
from pdlearn.fangtang import FangtangHandler
from pdlearn.dingding import DingDingHandler
from pdlearn.telegram import TelegarmHandler
import io
from PIL import Image
from pdlearn.config import cfg_get
import os
import base64  # 解码二维码图片

# 全局变量是否已经初始化
is_init = False
pushmode = "1"  # 0 不开启 1 钉钉 2 微信（并未实现） 3 Server 酱 4 pluspush 5 Telegram Bot
nohead = False
accesstoken = ""
secret = ""
islooplogin = False
zhuanxiang = False
scheme = ""
lock = False
stime = False
single = False


def init_global():
    """
    初始化全局变量
    """
    global nohead, islooplogin, single, scheme, pushmode, accesstoken, secret, zhuanxiang, is_init, lock, stime
    if os.getenv('Nohead') == "True":
        nohead = True

    if os.getenv('islooplogin') == "True":
        islooplogin = True

    if os.getenv('Single') == "True":
        single = True

    if os.getenv("Scheme") != None:
        scheme = os.getenv("Scheme")

    if os.getenv('Pushmode'):
        pushmode = os.getenv('Pushmode')
    else:
        pushmode = cfg_get("addition.Pushmode", "0")

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
    is_init = True


def pushprint(text):
    """
    推送或者显示
    """
    if nohead == True:
        print(accesstoken, secret)
        if pushmode == "1":
            push = DingDingHandler(accesstoken, secret)
            push.ddtextsend(text)
        elif pushmode == "3":
            push = FangtangHandler(accesstoken)
            push.fttext(text)
        elif pushmode == "4":
            push = PlusPushHandler(accesstoken)
            push.fttext(text)
        elif pushmode == "5":
            push = TelegarmHandler(accesstoken, secret)
            push.send_message(text)
    print(text)


def send_qrbase64(qcbase64):
    """
    推送登录二维码
    """
    if pushmode == "3":
        ft = FangtangHandler(accesstoken)
        ft.ftmsgsend(qcbase64)
    elif pushmode == "4":
        push = PlusPushHandler(accesstoken)
        push.ftmsgsend(qcbase64)
    elif pushmode == "5" and cfg_get("addition.telegram.send_qrimage", 0) == 1:
        img_b64decode = base64.b64decode(
            qcbase64[qcbase64.index(';base64,')+8:])
        push = TelegarmHandler(accesstoken, secret)
        push.send_qrurl(Image.open(io.BytesIO(img_b64decode)))
