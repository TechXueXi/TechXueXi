#!/bin/sh
# apt-get install supervisor

echo_supervisord_conf > /etc/supervisord.conf

sed -i -e 's/^file=\/tmp/file=\/var\/run/' \
    -e 's/^logfile=\/tmp/logfile=\/var\/log/' \
    -e 's/^pidfile=\/tmp/pidfile=\/var\/run/' \
    -e 's/^serverurl=unix:\/\/\/tmp/serverurl=unix:\/\/\/var\/run/' \
    /etc/supervisord.conf



cat >> /etc/supervisord.conf <<EOF

[program:xuexiwechat]
directory=/xuexi
user=root
command=/usr/local/bin/python wechatListener.py 
autostart=false
autorestart=true
stdout_logfile=/xuexi/user/wechat_listener.log
stderr_logfile=/xuexi/user/wechat_listener.log

EOF

cat >> /etc/supervisord.conf <<EOF

[program:xuexitg]
directory=/xuexi
user=root
command=/usr/local/bin/python telegramListener.py
autostart=false
autorestart=true
stdout_logfile=/xuexi/user/tg_listener.log
stderr_logfile=/xuexi/user/tg_listener.log

EOF

cat >> /etc/supervisord.conf <<EOF

[program:xuexiweb]
directory=/xuexi
user=root
command=/usr/local/bin/python webserverListener.py 
autostart=false
autorestart=true
stdout_logfile=/xuexi/user/web_listener.log
stderr_logfile=/xuexi/user/web_listener.log

EOF

mkdir -p /xuexi/user
cp -r /etc/supervisord.conf /xuexi/user/
#systemctl enable supervisord
#supervisorctl stop all
#supervisord -c /xuexi/user/supervisord.conf
#supervisorctl start all