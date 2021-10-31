from hashlib import sha1
import os
from flask import Flask, request
import requests
import json

from selenium.webdriver.support import ui
from pdlearn.config import cfg_get
from pdlearn.wechat import WechatHandler
from pdlearn.threads import MyThread
from pdlearn import file
import pandalearning as pdl

app = Flask(__name__)
appid = cfg_get("addition.wechat.appid", "")
appsecret = cfg_get("addition.wechat.appsecret", "")
token = cfg_get("addition.wechat.token", "")
openid = cfg_get("addition.wechat.openid", "")
wechat = WechatHandler()


class MessageInfo:
    to_user_name = ""
    from_user_name = ""
    create_time = ""
    msg_type = ""
    content = ""
    msg_id = ""
    event = ""
    event_key = ""

    def __init__(self, root):
        for child in root:
            if child.tag == 'ToUserName':
                self.to_user_name = child.text
            elif child.tag == 'FromUserName':
                self.from_user_name = child.text
            elif child.tag == 'CreateTime':
                self.create_time = child.text
            elif child.tag == 'MsgType':
                self.msg_type = child.text
            elif child.tag == 'Content':
                self.content = child.text
            elif child.tag == 'MsgId':
                self.msg_id = child.text
            elif child.tag == 'Event':
                self.event = child.text
            elif child.tag == 'EventKey':
                self.event_key = child.text


def get_update(timestamp, nonce):
    arguments = ''
    for k in sorted([token, timestamp, nonce]):
        arguments = arguments + str(k)
    m = sha1()
    m.update(arguments.encode('utf8'))
    return m.hexdigest()


def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    check = get_update(timestamp, nonce)
    return True if check == signature else False


def parse_xml(data):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    root = ET.fromstring(data)
    return MessageInfo(root)


def wechat_init():
    """
    初始化订阅号菜单
    """
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?"
    body = {
        "button": [
            {
                "type": "click",
                "name": "开始学xi",
                "key": "MENU_LEARN"
            },
            {
                "name": "我的",
                "sub_button": [
                        {
                            "type": "click",
                            "name": "今日积分",
                            "key": "MENU_SCORE"
                        },
                    {
                            "type": "click",
                            "name": "账号编码",
                            "key": "MENU_OPENID"
                            },
                ]
            }
        ]
    }

    res = requests.post(url=url, params={
        'access_token': wechat.get_access_token()
    }, data=json.dumps(body, ensure_ascii=False).encode('utf-8')).json()
    if res.get("errcode") == 0:
        wechat.send_text("菜单初始化成功，请重新关注订阅号")
    else:
        wechat.send_text(res.get("errmsg"))


def get_uid(oid):
    json_str = '''[]'''
    json_obj = file.get_json_data(
        "user/wechat_bind.json", json_str)
    wx_list = list(filter(lambda w: w["openId"] == oid, json_obj))
    if wx_list:
        return wx_list[0]["accountId"]
    else:
        return""


def wechat_get_openid(msg: MessageInfo):
    """
    获取用户的openId
    """
    wechat.send_text(msg.from_user_name, msg.from_user_name)


def wechat_learn(msg: MessageInfo):
    """
    开始学习
    """
    uid = get_uid(msg.from_user_name)
    if not uid:
        wechat.send_text("您未绑定账号，请联系管理员绑定", uid=msg.from_user_name)
    else:
        pdl.start(uid)


def wechat_get_score(msg: MessageInfo):
    """
    获取今日分数
    """
    uid = get_uid(msg.from_user_name)
    if not uid:
        wechat.send_text("您未绑定账号，请联系管理员绑定", uid=msg.from_user_name)
    else:
        score = pdl.get_my_score(uid)
        if not score:
            wechat.send_text("登录过期，请重新登录后再试", msg.from_user_name)
            pdl.add_user(msg.from_user_name)


def wechat_help():
    """
    获取帮助菜单
    """
    wechat.send_text(
        "/help 显示帮助消息\n/init 初始化订阅号菜单，仅需要执行一次\n/add 添加新账号\n/bind 绑定账号，如：/bind 账号编码 学xi编号\n/unbind 解除绑定 如：/unbind 账号编码")


def wechat_add():
    """
    添加新账号
    """
    pdl.add_user()


def wechat_bind(msg: MessageInfo):
    """
    绑定微信号
    """
    args = msg.content.split(" ")
    if len(args) == 3:
        json_str = '''[]'''
        json_obj = file.get_json_data(
            "user/wechat_bind.json", json_str)
        wx_list = list(filter(lambda w: w["openId"] == args[1], json_obj))
        if wx_list:
            index = json_obj.index(wx_list[0])
            json_obj[index]["accountId"] = args[2]
        else:
            json_obj.append({"openId": args[1], "accountId": args[2]})
        file.save_json_data("user/wechat_bind.json", json_obj)
        wechat.send_text("绑定成功")
    else:
        wechat.send_text("参数格式错误")


def wechat_unbind(msg: MessageInfo):
    """
    解绑微信号
    """
    args = msg.content.split(" ")
    if len(args) == 2:
        json_str = '''[]'''
        json_obj = file.get_json_data(
            "user/wechat_bind.json", json_str)
        wx_list = list(filter(lambda w: w["openId"] == args[1], json_obj))
        if wx_list:
            index = json_obj.index(wx_list[0])
            json_obj.pop(index)
            file.save_json_data("user/wechat_bind.json", json_obj)
            wechat.send_text("解绑成功")
        else:
            wechat.send_text("账号编码错误或该编码未绑定账号")
    else:
        wechat.send_text("参数格式错误")


@ app.route('/wechat', methods=['GET', 'POST'])
def weixinInterface():
    if check_signature:
        if request.method == 'GET':
            echostr = request.args.get('echostr', '')
            return echostr
        elif request.method == 'POST':
            data = request.data
            msg = parse_xml(data)
            if msg.msg_type == "event" and msg.event == "CLICK":
                if msg.event_key == "MENU_OPENID":
                    MyThread("get_user_openid", wechat_get_openid, msg).start()
                if msg.event_key == "MENU_LEARN":
                    MyThread("wechat_learn", wechat_learn, msg).start()
                if msg.event_key == "MENU_SCORE":
                    MyThread("wechat_get_score", wechat_get_score, msg).start()
            if msg.from_user_name == openid:
                if msg.content.startswith("/init"):
                    MyThread("wechat_init", wechat_init).start()
                if msg.content.startswith("/help"):
                    MyThread("wechat_help", wechat_help).start()
                if msg.content.startswith("/bind"):
                    MyThread("wechat_bind", wechat_bind, msg).start()
                if msg.content.startswith("/unbind"):
                    MyThread("wechat_unbind", wechat_unbind, msg).start()
                if msg.content.startswith("/add"):
                    MyThread("wechat_add", wechat_add).start()
            return "success"
    else:
        return 'signature error'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
