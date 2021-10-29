**[交流群地址及说明](https://github.com/TechXueXi/TechXueXi/issues/14)**

官方网站： https://techxuexi.js.org/

#### [其他运行方式](https://github.com/TechXueXi/TechXueXi/blob/dev/%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95-%E6%9B%B4%E6%96%B0%E6%96%B9%E6%B3%95-%E4%B8%8B%E8%BD%BD%E6%96%B9%E5%BC%8F.md)

#### 镜像地址： https://hub.docker.com/u/techxuexi/

**重要公告**： [公告栏（国内打不开）](https://t.me/s/techxuexi_notice) || [公告栏（国内可以打开）](https://notice.techxuexi.workers.dev)

**警告：如您不熟悉，请使用源码运行的方式**

## 有疑问？
遇到问题，请试着按如下步骤解决：

1. 仔细阅读过 `README.md` ， `使用方法-更新方法-下载方式.md` ， `DOCKER.md` 这些说明
2. 查看/搜索所有已有 issue，无论是open还是close的
3. 通过搜索引擎搜索，尝试不同的关键词 www.google.com www.baidu.com
4. 到提供的在线聊天室询问 (聊天室说明： https://github.com/TechXueXi/TechXueXi/issues/14 )
5. 提新 issue ，关注邮箱有关这个 issue 的提醒。

# 配置文件

由于Docker中的环境变量越来越多，可定义项目也逐渐增多，所以后续增加的部分配置项目移至配置文件。

所有可配置项目及说明，请参见[默认配置文件](https://github.com/npo5tech/TechXueXi/blob/dev/SourcePackages/config/default_template.conf)。

如需修改默认配置，请将虚拟目录`xuexi/user`映射至本地目录，首次运行后会产生`settings.conf`文件。该文件内首行代码不要删除。从第三行开始添加即可。

***请严格遵循书写规范*** 否则将导致程序无法运行。

**变量优先级**

环境变量 > settings.conf > default_template.conf



# Docker 地址

> 2021 年 9 月 25 日起 arm 和 amd 地址分开，请重新配置 docker

amd64（一般64位电脑，服务器）

```
docker pull techxuexi/techxuexi-amd64:{tag}
```

arm64（树莓派等）

```
docker pull techxuexi/techxuexi-arm64v8:{tag}
```

目前最新的 tag 请前往 https://hub.docker.com/u/techxuexi/ 查询

### 版本说明

分为开发版：tag含有dev，

稳定版： tag为 latest

# Docker 命令运行

注意短横线和冒号的位置。

```shell
docker run -e "AccessToken={token}" -e "Secret={密钥}" -d --name={容器名称} techxuexi/techxuexi-amd64:{tag}
```

上面命令的解释：

```shell
docker run -e "从下面参数处找到参数1" -e "从下面参数处找到参数2" -e "从下面参数处找到参数3" -d --name={容器名称} techxuexi/techxuexi-amd64:{tag}
```

请不要无脑照搬，需要修改。**请阅读本文档所有内容后再操作**

**如何登录** ： 设置推送方式之后， Docker 会发给你一个学习强国链接，用手机接收推送的链接，复制链接到学习#国 app，发给某个人，比如自己，再点击链接。也可以转二维码了扫描。**最简单的方法是设置环境变量 Scheme ，设置之后点击链接就能登录**

如果你是 `amd64` 的机器，那么就是 `techxuexi/techxuexi-amd64:{tag}`

如果你是 `arm64` 的机器，那么就是 `techxuexi/techxuexi-arm64v8:{tag}`

参数，输入时不输入`{}`

参考运行命令：

Docker 参考运行命令：

使用钉钉推送：

```
docker run \
-e "AccessToken=***" \
-e "Secret=***" \
-e "ZhuanXiang=True" \
-e "Pushmode=1" \
-e "Scheme=dtxuexi://appclient/page/study_feeds?url=" \
-v /volume1/docker/xuexi/user:/xuexi/user:rw \
-d --name=techxuexi --shm-size="2g" techxuexi/techxuexi-amd64:latest
```

使用 Telegram 推送 （推荐，但是需要翻墙）:

```
docker run \
-e "AccessToken=***" \
-e "Secret=***" \
-e "ZhuanXiang=True" \
-e "Pushmode=5" \
-e "Scheme=https://techxuexi.js.org/jump/techxuexi-20211023.html?" \
-v /volume1/docker/xuexi/user:/xuexi/user:rw \
-d --name=techxuexi --shm-size="2g" techxuexi/techxuexi-amd64:latest
```


# Docker 参数

参数  
tag=如果你是 amd64 的机器，那么就是 amd64，如果是 arm64 那么就是 arm64，然后后面跟版本号

##### 对于 Server 酱和 pluspush，只需要填写 token，而钉钉，TG 等机器人需要填写 token 和 secret

```
AccessToken=token
Secret=密码
```

```
Pushmode=1
```

表示：钉钉，其他见下方

### 必填
- AccessToken 。bot 发送指令的 token 具体方法参见下方 bot 指南
- Secret 钉钉推送时为钉钉 Secret，Telegram bot 则为管理员数字 Id
- Nohead 无窗口模式 默认值`True`，Docker 不要修改此参数
- Pushmode 消息推送模式：

  > 0 不开启

  > 1 钉钉

  > 2 微信（并未实现， https://github.com/orgs/TechXueXi/projects/2#card-66789077 ）

  > 3 Server 酱

  > 4 pluspush

  > 5 Telegram Bot **（推荐，支持指令交互，随时可以开始学习，需要翻墙）**

  > 6 WebPage

  **推送消息是为了把登录链接发送给你，现在请每天点击链接登录。**

##### 可选参数

- ZhuanXiang 环境变量，是否进行专项答题，默认False，docker模式下改成True也可以进行专项答题。设置`True`则开始答题，如果经常遇到视频题目，或者经常答题失败，建议关闭
- TZ 时区设置，默认值`Asia/Shanghai`
- CRONTIME Cron 参数，默认是`30 9 * * *`，即每天早上 9:30 执行 ,可以把 Cron 表达式放到这里去验证 https://crontab.guru/
- Sourcepath 项目源，默认是`https://github.com.cnpmjs.org/TechXueXi/TechXueXi.git`
- pullbranche 项目分支，默认是`dev`，后续可能会变为`master`
- islooplogin 循环参数，默认`False`，当设置为`True`的时候，如果扫码超时会一直尝试循环获取新的扫码，考虑到微信公众号推送有次数限制，慎用
- MaxScore 达到指定分数停止学习（未实现，开发团队成员可查看 https://github.com/orgs/TechXueXi/projects/2#card-70976956 ）
- **配置项（不是环境变量）** answer_error_max，默认值100，可以修改找不到答案时尝试的次数，仅Docker中有效
- **没有找到的环境变量，请查看上方提到过的默认配置文件，可能做成了配置项**

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

```
single=1 不想并发，单线程
```

**设置了下面这个，点击发送的链接可以直接打开学习强国** 。如果用钉钉推送可以如下设置（钉钉支持 dtxuexi 协议）：

```
Scheme=dtxuexi://appclient/page/study_feeds?url=
```

也可以自己搭建跳板，从网页跳转。公告栏有 php 的跳板可以下载使用。

不会或者不想自己搭建，可以使用我们提供的：

```
Scheme=https://techxuexi.js.org/jump/techxuexi-20211023.html?
```

但是不保证稳定。 ~~techxuexi太好用了~~ ， https://techxuexi.js.org 这个地址已经被国内浏览器加进黑名单了 ~~中国大陆官方认证~~ ，默认浏览器不要用国内的，不然提示危险网页。现在 gfw 还没墙，只是国产浏览器的黑名单屏蔽。

其他的设置方法去群里问~~大佬~~同志们吧。

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
version: '3.5'
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
    build:
      context: .
      shm_size: '2gb' 
    shm_size: '2gb'
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
3. 在 Tg 中搜索[`@userinfobot`](https://t.me/userinfobot)，点击`START`，它就会给你发送你的信息，记住 Id 即可，是一串数字。
4. 跟你创建的 bot 会话，点击`START`，或者发送`/start`
5. 将第 2 步获取的 token 放在`AccessToken`中，第 3 步获取的 Id 放到`Secret`中，`Pushmode`设置为 5。

增加telegram bot指令支持

`/help` 获取帮助

`/learn` 开始学习，`/learn 张三` 指定账号学习

`/list` 获取账号列表，获取有效的cookie列表，显示过期时间，并显示当天学习积分。

`/add` 添加新账号，只添加账号，不会立即学习

`/update` 更新本地代码， `/update`指令支持参数 如`/update --rebase`

**注意，用学习强国官方软件及网页时关闭翻墙软件**。但是telegram推送需要翻墙。

**bot使用代理说明：进入容器内找到user/settings.conf，根据本库的default_template.conf文件里addition附加功能-telegram的相关内容复制进去、填写好保存即可。）**
支持http和socks5两种代理方式

**要做好分流**

# 其他说明

多账号：

方法一，一个群（钉钉，telegram）里拉多个人，定多个时，启动多次

方法二，多创建几个容器，一个容器一个人，给每个人配置推送登录链接。

其他没有固定下来的用法，请加群了解。

# Web网页控制台

参考 telegram 需要打开端口映射

docker指令
```sh


docker run \
  -e "AccessToken=***" \
  -e "Secret=***" \
  -e "ZhuanXiang=True" \
  -e "Pushmode=1" \
  -e "Scheme=https://techxuexi.js.org/jump/techxuexi-20211023.html?" \
  -v /volume1/docker/xuexi/user:/xuexi/user:rw \
  -d --name=techxuexi --shm-size="2g" \
  -p 9980:80 \
  techxuexi/techxuexi-amd64:latest
   
```
docker-config.yaml配置
```yaml
version: '3.5'
services:
  xuexi:
    image: techxuexi/techxuexi-amd64
    container_name: xuexi
    restart: unless-stopped
    ports:
      - 9980:80/tcp
    volumes:
       - ./user:/xuexi/user
    environment:
      - Scheme=https://techxuexi.js.org/jump/techxuexi-20211023.html?
      - ZhuanXiang=True
      - Pushmode=6
      - CRONTIME=30 9 * * *
    build:
      context: .
      shm_size: '2gb' 
    shm_size: '2gb'

```


**[交流群地址及说明](https://github.com/TechXueXi/TechXueXi/issues/14)**

## Docker 如果发给你一个学习强国链接，不是让你下载，是让你登录，复制链接到学习#国 app，发给某个人，比如自己，再点击链接


退出登录，多个不同用户使用，删掉 user/cookie.json 文件

chrome crash 的原因是 docker 虚拟机共享内存不足,创建 docker 时设置 --shm-size="2g"

可参考 https://github.com/TechXueXi/TechXueXi/issues/82

https://stackoverflow.com/questions/30210362/how-to-increase-the-size-of-the-dev-shm-in-docker-container

也可以参考 https://t.me/techxuexi_notice/49


