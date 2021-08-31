import requests  # 导入依赖库
class FangtangHandler:
    def __init__(self, token):
        self.token = token
    def ftmsgsend(self, msgurl):
           
            url="https://sctapi.ftqq.com/{}.send".format(
            self.token
            )
            headers = {"Content-Type": "application/x-www-form-urlencoded"}  # 定义数据类型
            data = {
                "title": "学 xi 强 guo ",
                "desp":"![avatar][base64str]\n[base64str]:"+msgurl
            }

            res = requests.post(url, data=data, headers=headers)  # 发送post请求
            print(res.text)
    def fttext(self,text):
            url="https://sctapi.ftqq.com/{}.send".format(
                self.token
                )
            headers = {"Content-Type": "application/x-www-form-urlencoded"}  # 定义数据类型
            data = {
                    "title": "学 xi 强 guo ",
                    "desp": text
                }

            res = requests.post(url, data=data, headers=headers)  # 发送post请求
            print(res.text)
