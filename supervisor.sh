#!/bin/sh
# apt-get install supervisor

echo_supervisord_conf > /etc/supervisord.conf

cat >> /etc/supervisord.conf <<EOF

[program:xuexitg]
directory=/xuexi
command=/usr/local/bin/python /xuexi/telegramListener.py
autostart=true
autorestart=true

EOF