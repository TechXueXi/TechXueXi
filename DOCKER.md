# Docker运行命令
```shell
docker run -e "AccessToken={token}" -e "Secret={密钥}" -d --name={容器名称} techxuexi/techxuexi:{tag}
```
参数  
tag=如果你是amd64的机器，那么就是amd64，如果是arm64那么就是arm64，然后后面跟版本号,例如 techxuexi/techxuexi:amd64-40   techxuexi/techxuexi:arm64-40  
##### 对于Server酱和pluspush，只需要填写token，而钉钉机器人需要填写token和secret
```
AccessToken=token  
Secret=密码  
```
```
Pushmode=推送模式，1表示：钉钉，2表示：微信（并未实现），3表示：Server酱，4表示：pluspush，0表示不开启  
```
##### 可选参数  
```
CRONTIME=Cron参数，默认是30 9 * * *，既每天早上9:30执行  
```
```
Sourcepath=项目源，默认是https://github.com.cnpmjs.org/TechXueXi/TechXueXi.git
```
```
pullbranche=项目分支，默认是dev，后续可能会变为master
```
```
islooplogin=循环参数，当设置为True的时候，如果扫码超时会一直尝试循环获取新的扫码，考虑到微信公众号推送有次数限制，慎用
```
##### 钉钉机器人接入方式请参考 https://developers.dingtalk.com/document/app/custom-robot-access/title-72m-8ag-pqw
##### Server酱接入参考 http://www.pushplus.plus
##### pluspush介入参考 http://pushplus.com