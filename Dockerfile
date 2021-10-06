  
FROM python:3.7-slim
ARG usebranche="dev"
ENV pullbranche=${usebranche}
RUN apt-get update
RUN apt-get install -y wget unzip libzbar0 git cron
ENV TZ=Asia/Shanghai
ENV AccessToken=
ENV Secret=
ENV Nohead=True
ENV Pushmode=1
ENV islooplogin=False
ENV Sourcepath="https://github.com.cnpmjs.org/TechXueXi/TechXueXi.git"
ENV CRONTIME="30 9 * * *"
# RUN rm -f /xuexi/config/*; ls -la
COPY requirements.txt /xuexi/requirements.txt
COPY run.sh /xuexi/run.sh 
COPY start.sh /xuexi/start.sh 
RUN pip install -r /xuexi/requirements.txt
RUN cd /xuexi/; wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_92.0.4515.159-1_amd64.deb; dpkg -i google-chrome-stable_92.0.4515.159-1_amd64.deb; apt-get -fy install; google-chrome --version; rm -f google-chrome-stable_92.0.4515.159-1_amd64.deb
RUN cd /xuexi/; wget -O chromedriver_linux64_92.0.4515.107.zip http://npm.taobao.org/mirrors/chromedriver/92.0.4515.107/chromedriver_linux64.zip; unzip chromedriver_linux64_92.0.4515.107.zip; chmod 755 chromedriver; ls -la; ./chromedriver --version

WORKDIR /xuexi
RUN chmod +x ./run.sh
RUN chmod +x ./start.sh
RUN mkdir code
WORKDIR /xuexi/code
RUN git clone -b ${pullbranche} ${Sourcepath}
WORKDIR /xuexi
ENTRYPOINT ["/bin/bash", "./start.sh"]
