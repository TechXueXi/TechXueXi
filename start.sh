#!/bin/sh
if ! git -C /xuexi/code/TechXueXi config pull.ff only; then
    rm -rf /xuexi/code/TechXueXi
    cd /xuexi/code/ && git clone -b ${pullbranche} ${Sourcepath}
fi
printenv >> /etc/environment
touch /var/log/cron.log
echo "接下来开始启动 Telegram 机器人  "
./run.sh 2>&1 & nohup /usr/local/bin/python /xuexi/telegramListener.py & 
echo -e "$CRONTIME $USER /xuexi/run.sh >> /var/log/cron.log 2>&1\n#empty line" > /etc/cron.d/mycron
crontab /etc/cron.d/mycron
cron && tail -f /var/log/cron.log
