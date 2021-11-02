from hashlib import sha1
import os
import time
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

    def returnXml(self, msg, msg_type="text"):
        return f"<xml><ToUserName><![CDATA[{self.from_user_name}]]></ToUserName><FromUserName><![CDATA[{self.to_user_name}]]></FromUserName><CreateTime>{time.time()}</CreateTime><MsgType><![CDATA[{msg_type}]]></MsgType><Content><![CDATA[{msg}]]></Content></xml>"


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


def wechat_init(msg: MessageInfo):
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
        return msg.returnXml("菜单初始化成功，请重新关注订阅号")
    else:
        return msg.returnXml(res.get("errmsg"))


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
    return msg.returnXml(msg.from_user_name)


def wechat_learn(msg: MessageInfo):
    """
    开始学习
    """
    uid = get_uid(msg.from_user_name)
    if not uid:
        msg: MessageInfo("您未绑定账号，请联系管理员绑定")
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


def wechat_help(msg: MessageInfo):
    """
    获取帮助菜单
    """
    return msg.returnXml(
        "/help 显示帮助消息\n/init 初始化订阅号菜单，仅需要执行一次\n/add 添加新账号\n/bind 绑定账号，如：/bind 账号编码 学xi编号\n/unbind 解除绑定 如：/unbind 账号编码\n/list 获取全部账号信息\n/update 更新程序")


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
        return msg.returnXml("绑定成功")
    else:
        return msg.returnXml("参数格式错误")


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
            return msg.returnXml("解绑成功")
        else:
            return msg.returnXml("账号编码错误或该编码未绑定账号")
    else:
        return msg.returnXml("参数格式错误")


def wechat_list(msg: MessageInfo):
    """
    获取全部成员
    """
    msg = pdl.get_user_list()
    wechat.send_text(msg)


def wechat_admin_learn(msg: MessageInfo):
    """
    学习
    """


def wechat_update(msg: MessageInfo):
    res = ""
    try:
        shell = "git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche "
        params = msg.content.split(" ")
        if len(params) > 1:
            shell += params[1]
        msg = os.popen(shell).readlines()[-1]
        if "up to date" in msg:
            res = "当前代码已经是最新的了"
        else:
            os.popen("cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi")
            res = "代码更新完成"+msg
    except Exception as e:
        res = "更新失败："+str(e)
    wechat.send_text(res)


@app.route('/wechat', methods=['GET', 'POST'])
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
                    return wechat_get_openid(msg)
                if msg.event_key == "MENU_LEARN":
                    MyThread("wechat_learn", wechat_learn, msg).start()
                if msg.event_key == "MENU_SCORE":
                    MyThread("wechat_get_score", wechat_get_score, msg).start()
            if msg.from_user_name == openid:
                if msg.content.startswith("/init"):
                    return wechat_init(msg)
                if msg.content.startswith("/help"):
                    return wechat_help(msg)
                if msg.content.startswith("/bind"):
                    return wechat_bind(msg)
                if msg.content.startswith("/unbind"):
                    return wechat_unbind(msg)
                if msg.content.startswith("/add"):
                    MyThread("wechat_add", wechat_add).start()
                if msg.content.startswith("/list"):
                    MyThread("wechat_list", wechat_list, msg).start()
                if msg.content.startswith("/learn"):
                    MyThread("wechat_admin_learn",
                             wechat_admin_learn, msg).start()
                if msg.content.startswith("/update"):
                    MyThread("wechat_update",
                             wechat_update, msg).start()
            return "success"
    else:
        return 'signature error'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
