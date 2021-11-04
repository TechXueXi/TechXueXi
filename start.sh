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

if [ "${Pushmode}" = "5" ]; then
    echo "当前模式为网页控制台模式，即将启动守护 --  xuexitg"
    sleep 1
    supervisord -c /etc/supervisord.conf
    # nohup /usr/local/bin/python /xuexi/telegramListener.py >> /xuexi/user/tg_listener.log 2>&1 &
    sleep 1
    supervisorctl start xuexitg
fi
if [ "${Pushmode}" = "2" ]; then
    nohup /usr/local/bin/python /xuexi/wechatListener.py >> /xuexi/user/wechat_listener.log 2>&1 &
fi
if [ "${Pushmode}" = "6" ]; then
    echo "当前模式为网页控制台模式，即将启动守护 --  xuexiweb"
    : > /var/log/xuexi-web.log 
    sleep 1
    supervisord -c /etc/supervisord.conf
    sleep 1
    # nohup /usr/local/bin/python /xuexi/telegramListener.py >> /xuexi/user/tg_listener.log 2>&1 &
    sleep 1
    # nohup /usr/local/bin/python /xuexi/telegramListener.py >> /xuexi/user/tg_listener.log 2>&1 &
    supervisorctl start xuexiweb
    tail -f /var/log/xuexi-web.log &
fi
./run.sh 2>&1 &
echo -e "$CRONTIME $USER /xuexi/run.sh >> /var/log/cron.log 2>&1\n#empty line" >/etc/cron.d/mycron
crontab /etc/cron.d/mycron
cron && tail -f /var/log/cron.log
