##是否是无界面模式，一般用在命令行，docker上
from pdlearn.pluspush import PlusPushHandler
from pdlearn.fangtang import FangtangHandler
from pdlearn.dingding import DingDingHandler

pushmode ="1"
nohead = False
accesstoken = ""
secret=""
islooplogin=False
##推送或者显示
def pushprint(text):
    print(accesstoken,secret)
    if nohead==True:
       if pushmode=="1":
            push=DingDingHandler(accesstoken,secret)
            push.ddtextsend(text)
       elif pushmode=="3":
            push=FangtangHandler(accesstoken)
            push.fttext(text)
       elif pushmode=="4":
            push=PlusPushHandler(accesstoken)
            push.fttext(text)

    print(text)