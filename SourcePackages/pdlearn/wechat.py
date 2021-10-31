import requests
import json
from pdlearn.config import cfg_get
from pdlearn import file
import time


class WechatHandler:
    def __init__(self):
        self.token = []
        self.token = self.get_access_token()
        self.openid = cfg_get("addition.wechat.openid", "")

    def get_access_token(self, refresh=False):
        if not refresh:
            # 检查变量
            if self.token and self.token[1] > time.time():
                return self.token
            # 检查文件
            template_json_str = '''[]'''
            token_json_obj = file.get_json_data(
                "user/wechat_token.json", template_json_str)
            if token_json_obj and token_json_obj[1] > time.time():
                self.token = token_json_obj
                return self.token
        # 获取新token
        appid = cfg_get("addition.wechat.appid", "")
        appsecret = cfg_get("addition.wechat.appsecret", "")
        url_token = 'https://api.weixin.qq.com/cgi-bin/token?'
        res = requests.get(url=url_token, params={
            "grant_type": 'client_credential',
            'appid': appid,
            'secret': appsecret,
        }).json()
        token = res.get('access_token')
        expires = int(res.get('expires_in'))-10+time.time()
        self.token = [token, expires]
        file.save_json_data("user/wechat_token.json", self.token)
        return self.token

    def send_text(self, text, uid=""):
        if not uid:
            uid = self.openid
        token = self.get_access_token()
        url_msg = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?'
        body = {
            "touser": uid,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        res = requests.post(url=url_msg, params={
            'access_token': token
        }, data=json.dumps(body, ensure_ascii=False).encode('utf-8')).json()
        print(res)
        if res["errcode"] == 40001:
            self.get_access_token(True)
            self.send_text(text, uid)

    def get_opendid_by_uid(self, uid):
        """
        账号换绑定的openid，没有则返回主账号
        """
        json_str = '''[]'''
        json_obj = file.get_json_data(
            "user/wechat_bind.json", json_str)
        wx_list = list(
            filter(lambda w: w["accountId"] == uid or w["openId"] == uid, json_obj))
        if wx_list:
            return wx_list[0]["openId"]
        else:
            return self.openid
