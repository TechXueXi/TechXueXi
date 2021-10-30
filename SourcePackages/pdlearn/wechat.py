import requests
import json
from pdlearn.config import cfg_get
import time


class WechatHandler:
    def __init__(self):
        self.token = []
        self.token = self.get_access_token()
        self.openid = cfg_get("addition.wechat.openid", "")

    def get_access_token(self):
        if self.token and self.token[1] > time.time():
            return self.token
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
        return self.token

    def send_text(self, text):
        token = self.get_access_token()
        url_msg = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?'
        body = {
            "touser": self.openid,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        requests.post(url=url_msg, params={
            'access_token': token
        }, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
