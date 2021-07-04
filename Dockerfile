FROM python:3.7-slim

RUN apt-get update
RUN apt-get install -y wget unzip libzbar0
COPY SourcePackages/ /xuexi
# RUN rm -f /xuexi/config/*; ls -la
COPY requirements.txt /xuexi/requirements.txt
RUN pip install -r /xuexi/requirements.txt
RUN cd /xuexi/; wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_80.0.3987.163-1_amd64.deb; dpkg -i google-chrome-stable_80.0.3987.163-1_amd64.deb; apt-get -fy install; google-chrome --version; rm -f google-chrome-stable_80.0.3987.163-1_amd64.deb
RUN cd /xuexi/; wget -O chromedriver_linux64_80.0.3987.106.zip http://npm.taobao.org/mirrors/chromedriver/80.0.3987.106/chromedriver_linux64.zip; unzip chromedriver_linux64_80.0.3987.106.zip; chmod 755 chromedriver; ls -la; ./chromedriver --version

WORKDIR /xuexi