更新了环境适配玩客云盒子armbian 32位arm docker编译
Docker-compose 设置
```
version: '3.5'
services:
  xuexi:
    image: xuexi:arm
    container_name: xuexi
    restart: unless-stopped
    volumes:
       - ./user:/xuexi/user
    environment:
      - AccessToken=
      - Secret=
      - Pushmode=1
      - CRONTIME=30 0-23/8 * * *
    build:
      context: .
      shm_size: '2gb' 
    shm_size: '2gb'
```
由于cookie有效期为12小时，CRONTIME可以设置为 30 0-23/8 * * * 每8小时执行一次
原文参考：
https://github.com/TechXueXi/TechXueXi
