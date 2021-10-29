#!/bin/sh
# apt-get install supervisor

echo_supervisord_conf > /etc/supervisord.conf

sed -i -e 's/^file=\/tmp/file=\/var\/run/' \
    -e 's/^logfile=\/tmp/logfile=\/var\/log/' \
    -e 's/^pidfile=\/tmp/pidfile=\/var\/run/' \
    -e 's/^serverurl=unix:\/\/\/tmp/serverurl=unix:\/\/\/var\/run/' \
    /etc/supervisord.conf

cat >> /etc/supervisord.conf <<EOF

[program:xuexitg]
directory=/xuexi
user=root
command=/usr/local/bin/python telegramListener.py
autostart=true
autorestart=true

[program:xuexiweb]
directory=/xuexi
user=root
command=/usr/local/bin/python webserverListener.py
autostart=true
autorestart=true

EOF