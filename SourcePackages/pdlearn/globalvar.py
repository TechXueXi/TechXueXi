##是否是无界面模式，一般用在命令行，docker上
from SourcePackages.pdlearn.dingding import DingDingHandler


nohead = False
accesstoken = ""
secret=""
##推送或者显示
def pushprint(text):
    if nohead==True:
       push=DingDingHandler(accesstoken,secret)
       push.ddtextsend(text)
    print(text)