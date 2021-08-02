# -*- coding: utf-8 -*-
"""
利用企业微信的应用接口，来发送消息和图片。需要先加入企业微信
"""

import time
import requests
import json

class WeChat:
    
    #初始化参数
    def __init__(self):
        self.CORPID = ''  #企业ID，在管理后台获取
        self.CORPSECRET = ''#自建应用的Secret，每个自建应用里都有单独的secret 
        self.AGENTID = ''  #应用ID，在后台应用中获取
        self.TOUSER = ""  # 接收者用户名,多个用户用|分割
        
    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,'corpsecret': self.CORPSECRET,}
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        #print (data)
        return data["access_token"]
    
    def get_access_token(self):
        try:
            with open('access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7200:#token的有效时间7200s
                return access_token
            else:
                with open('access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    #发送文本消息
    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            #"toparty": self.TOPARY, 	#设置给部门发送
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
            "content": message
            },
            "safe": "0"
        }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()#当返回的数据是json串的时候直接用.json即可将respone转换成字典
        #print (respone["errmsg"])
        return respone["errmsg"]
    
     ##上传到图片素材，返回'media_id'，改动下type类型就可以获取其他类型文件的id
    def get_media_url(self, path): 
        Gtoken = self.get_access_token()
        #此句话用来上传临时文件，type可以是图片（image）、语音（voice）、视频（video），普通文件（file）
        img_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}".format(Gtoken) + '&type=image'
        #下面的是用来上传永久的图片
        #img_url = "https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg?access_token={}".format(Gtoken)
        """下面是读取文件的部分
        with open(path,'rb') as f:
            files = {'media': f}
            r = requests.post(img_url, files=files)
        
        """
        #不读取文件，直接由网上读取图像数据
        files = {'media': path}
        r = requests.post(img_url, files=files)
        re = r.json()
        #re = json.loads(r.text)
        #会有不同返回值，具体见https://work.weixin.qq.com/api/doc/90000/90135/90253
        #print("media_id: " + re['media_id'])
        return re['media_id']
    
    #发送图片
    def send_image(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            #"toparty": self.TOPARY, 	#设置给部门发送
            "msgtype": "image",
            "agentid": self.AGENTID,
            "image": {
            "media_id" : message
            },
            "safe": "0"
        }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()#当返回的数据是json串的时候直接用.json即可将respone转换成字典
        #print (respone["errmsg"])
        return respone["errmsg"]
        

        
if __name__ == '__main__':
        
    wx = WeChat()
    #发送消息示例  
    wx.send_data("这是程序发送的第1条消息！\n Python程序调用企业微信API,从自建应用“告警测试应用”发送给管理员的消息！")
    #发送图片示例
    #wx.send_image(wx.get_media_url("C:\\Users\\Sean\Desktop\\2.jpg"))