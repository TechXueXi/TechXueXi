#!/bin/bash

update() {

    echo "检查更新"
    git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche
    echo "检查更新完毕"
    cp /xuexi/code/TechXueXi/*.sh /xuexi
    cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
    echo "下载更新"
    git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche
    echo "下载完毕"
    cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
    echo "更新完成"
}

if [[ ${pullbranche} == "developing" ]]; then
    echo "当前处于开发模式，自动更新"
    update
fi
#echo "检查更新"
#git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche
#echo "检查更新完毕"
#cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi


#if ! git -C /xuexi/code/TechXueXi config pull.ff only; then
#    rm -rf /xuexi/code/TechXueXi
#    cd /xuexi/code/ && git clone -b ${pullbranche} ${Sourcepath}
#fi
printenv >>/etc/environment
touch /var/log/cron.log

#TODO : 日志时间后缀，记得将 supervisor.sh 一起改了
LOG_SUFFIX=$(date +"%Y-%m-%d--%H-%M-%S")

if [ "${Pushmode}" = "2" ]; then
    echo "当前模式为 Wechat 模式，即将启动守护 --  xuexiwechat"
    : > /xuexi/user/wechat_listener.log
    sleep 1
    ./supervisor.sh 2>&1 & #修复Error:could not find config file /xuexi/user/supervisord.conf的问题
    supervisord -c /xuexi/user/supervisord.conf
    sleep 1
    supervisorctl start xuexiwechat
    if [ $? -ne 0 ]; then
        echo "守护进程启动失败，切换备用方式"
        nohup /usr/local/bin/python /xuexi/wechatListener.py >> /xuexi/user/wechat_listener.log 2>&1 &
    fi
    tail -f /xuexi/user/wechat_listener.log &
fi


if [ "${Pushmode}" = "5" ]; then
    echo "当前模式为 Telegram 模式，即将启动守护 --  xuexitg"
    : > /xuexi/user/tg_listener.log
    sleep 1
    ./supervisor.sh 2>&1 & #修复Error:could not find config file /xuexi/user/supervisord.conf的问题
    supervisord -c /xuexi/user/supervisord.conf
    if [ $? -ne 0 ]; then
        echo "守护进程启动失败，切换备用方式"
        nohup /usr/local/bin/python /xuexi/telegramListener.py >> /xuexi/user/tg_listener.log 2>&1 &
    fi
    sleep 1
    supervisorctl start xuexitg
    tail -f /xuexi/user/tg_listener.log &
fi


if [ "${Pushmode}" = "6" ]; then
    echo "当前模式为 WEB网页控制台 模式，即将启动守护 --  xuexiweb"
    : > /xuexi/user/web_listener.log
    sleep 1
    ./supervisor.sh 2>&1 & #修复Error:could not find config file /xuexi/user/supervisord.conf的问题
    supervisord -c /xuexi/user/supervisord.conf
    sleep 1
    supervisorctl start xuexiweb
    if [ $? -ne 0 ]; then
        echo "守护进程启动失败，切换备用方式"
        nohup /usr/local/bin/python /xuexi/webserverListener.py >> /xuexi/user/web_listener.log 2>&1 &
    fi
    tail -f /xuexi/user/web_listener.log &
fi

./run.sh 2>&1 &
echo -e "$CRONTIME $USER /xuexi/run.sh >> /var/log/cron.log 2>&1\n#empty line" >/etc/cron.d/mycron
crontab /etc/cron.d/mycron
cron && tail -f /var/log/cron.log
