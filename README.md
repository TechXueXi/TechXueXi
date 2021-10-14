更新了环境适配玩客云盒子armbian 32位arm docker编译
Docker-compose 设置
```
version: '2.1'
services:
  xuexi:
    image: techxuexi/techxuexi-amd64:XXX
    container_name: xuexi
    restart: unless-stopped
    volumes:
       - ./user:/xuexi/user
    environment:
      - AccessToken=
      - Secret=
      - Pushmode=
      - CRONTIME=30 0/8 * * *
```
由于cookie有效期为12小时，CRONTIME可以设置为 30 0/8 * * * 每8小时30分执行一次
原文参考：
https://github.com/TechXueXi/TechXueXi
