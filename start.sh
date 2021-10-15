#!/bin/sh
if ! git -C /xuexi/code/TechXueXi config pull.ff only; then
    rm -rf /xuexi/code/TechXueXi
    cd /xuexi/code/ && git clone -b ${pullbranche} ${Sourcepath}
fi
printenv >> /etc/environment
touch /var/log/cron.log
if [ "${Pushmode}" = "5" ]; then
    # supervisord -c /etc/supervisord.conf
    nohup /usr/local/bin/python /xuexi/telegramListener.py >> /xuexi/user/tg_listener.log 2>&1 &
fi
./run.sh 2>&1 & 
echo -e "$CRONTIME $USER /xuexi/run.sh >> /var/log/cron.log 2>&1\n#empty line" > /etc/cron.d/mycron
crontab /etc/cron.d/mycron
cron && tail -f /var/log/cron.log
