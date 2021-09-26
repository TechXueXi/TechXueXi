**[交流群地址及说明](https://github.com/TechXueXi/TechXueXi/issues/14)**

#### [其他运行方式](https://github.com/TechXueXi/TechXueXi/blob/dev/%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95-%E6%9B%B4%E6%96%B0%E6%96%B9%E6%B3%95-%E4%B8%8B%E8%BD%BD%E6%96%B9%E5%BC%8F.md)

#### 镜像地址： https://hub.docker.com/u/techxuexi/

# Docker 地址

2021 年 9 月 25 日起 arm 和 amd 地址分开

arm64

```
docker pull techxuexi/techxuexi-arm64v8:{tag}
```

amd64

```
docker pull techxuexi/techxuexi-amd64:{tag}
```

目前最新的 tag 请前往 https://hub.docker.com/u/techxuexi/ 查询

# Docker 参数

- TZ 时区设置，默认值`Asia/Shanghai`
- AccessToken bot 发送指令的 token 具体方法参见下方 bot 指南
- Secret 钉钉推送时为钉钉 Secret，Telegram bot 则为管理员数字 Id
- Nohead 无窗口模式 默认值`True`，Docker 不要修改此参数
- Pushmode 消息推送模式

  > 0 不开启

  > 1 钉钉

  > 2 微信（并未实现）

  > 3 Server 酱

  > 4 pluspush

  > 5 Telegram Bot

- CRONTIME Cron 参数，默认是`30 9 * * *`，即每天早上 9:30 执行 ,可以把 Cron 表达式放到这里去验证 https://crontab.guru/
- Sourcepath 项目源，默认是`https://github.com.cnpmjs.org/TechXueXi/TechXueXi.git`
- pullbranche 项目分支，默认是`dev`，后续可能会变为`master`
- islooplogin 循环参数，默认`False`，当设置为`True`的时候，如果扫码超时会一直尝试循环获取新的扫码，考虑到微信公众号推送有次数限制，慎用

# Docker 命令运行

```shell
docker run -e "AccessToken={token}" -e "Secret={密钥}" -d --name={容器名称} techxuexi/techxuexi:{tag}
```

```shell
docker run -e "从Docker.md找到参数1" -e "从Docker.md找到参数2" -e "从Docker.md找到参数3" -d --name={容器名称} techxuexi/techxuexi:{tag}
```

请不要无脑照搬，需要修改

参数，输入时不输入`{}`

参数  
tag=如果你是 amd64 的机器，那么就是 amd64，如果是 arm64 那么就是 arm64，然后后面跟版本号,例如 techxuexi/techxuexi:amd64-40 techxuexi/techxuexi:arm64-40

##### 对于 Server 酱和 pluspush，只需要填写 token，而钉钉，TG等机器人需要填写 token 和 secret

```
AccessToken=token
Secret=密码
```

```
Pushmode=1
```

表示：钉钉，其他见上方

##### 可选参数

```
CRONTIME=Cron参数，默认是30 9 * * *，即每天早上9:30执行  ,可以把Cron表达式放到这里去验证 https://crontab.guru/
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

# 群晖 Docker 设置

Docker 的安装就不赘述，直接从搜索注册表开始

在注册表中搜索`techxuexi`根据你的版本，选择 arm 或者 amd 进行下载
![image](https://user-images.githubusercontent.com/91232777/134791915-2a49ff12-56ed-4808-8400-58c5c491757b.png)

下载完成之后，到镜像中双击启动
![image](https://user-images.githubusercontent.com/91232777/134791968-1f206822-2d67-496c-884d-7ec51d446b85.png)
点击`高级设置`

- 映射虚拟目录 `可选`，此操作方便修改 config 文件

  点击`添加文件夹`

  文件夹选择群晖里创建的某个文件夹，挂载路径输入`/xuexi/user`
  ![image](https://user-images.githubusercontent.com/91232777/134792036-88d34874-6be0-4fc9-b733-cfa8d82c2804.png)

- 设置环境变量 各个变量具体值参照上方说明

  建议根据个人需求设置`AccessToken`、`Secret`、`Pushmode`、`CRONTIME`。其他值不建议更改。
  ![image](https://user-images.githubusercontent.com/91232777/134792091-e2e504cb-4bb6-44ff-86fc-783cd3508a44.png)

设置完成之后，下一步运行即可。
![image](https://user-images.githubusercontent.com/91232777/134792177-0465276b-00ef-4513-9cc7-c39f253d82b0.png)

# Docker-compose 设置

在文件夹中创建`docker-compose.yml`文件、`user`文件夹，

```
version: '2.1'
services:
  xuexi:
    image: techxuexi/techxuexi-amd64:dev53
    container_name: xuexi
    restart: unless-stopped
    volumes:
       - ./user:/xuexi/user
    environment:
      - AccessToken=
      - Secret=
      - Pushmode=
      - CRONTIME=30 9 * * *
```

根据个人需求修改 yml 文件，然后运行`docker-compose up -d`启动即可

# 通知机器人配置

## 钉钉机器人

接入方式请参考 https://developers.dingtalk.com/document/app/custom-robot-access/title-72m-8ag-pqw

## Server 酱

接入参考 https://sct.ftqq.com/

## pluspush

接入参考 http://www.pushplus.plus

## Telegram Bot

1. 在 Tg 中搜索[`@BotFather`](https://t.me/BotFather)，发送指令`/newbot`创建一个 bot
2. 获取你创建好的 API Token 格式为`123456789:AAaaaa-Uuuuuuuuuuu`,要完整复制**全部内容**
3. 在 Tg 中搜索[`@userinfobot`](https://t.me/userinfobot)，点击`START`，它就会给你发送你的信息，记住 Id 即可，是一串 9 位的数字。
4. 跟你创建的 bot 会话，点击`START`，或者发送`/start`
5. 将第 2 步获取的 token 放在`AccessToken`中，第 3 步获取的 Id 放到`Secret`中，`Pushmode`设置为 5。

# 其他说明

多账号等其他没有固定下来的用法，请加群了解。

**[交流群地址及说明](https://github.com/TechXueXi/TechXueXi/issues/14)**

## Docker 如果发给你一个学习强国链接，不是让你下载，是让你登录，复制链接到学习#国 app，发给某个人，比如自己，再点击链接
