#!/bin/sh
touch /var/log/cron.log
./run.sh >> /var/log/cron.log 2>&1 &
echo -e "$CRONTIME /xuexi/run.sh >> /var/log/cron.log 2>&1\n#empty line" > /etc/cron.d/mycron
crontab /etc/cron.d/mycron
cron && tail -f /var/log/cron.log
