# Docker运行命令
```shell
docker run -e "AccessToken={钉钉的token}" -e "Secret={钉钉机器人的密钥}" -d --name={容器名称} {镜像}
```
参数
AccessToken=钉钉的token
Secret=钉钉的密码
可选参数
CRONTIME=Cron参数，默认是30 9 * * *，既每天早上9:30执行
