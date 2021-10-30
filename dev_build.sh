#!/bin/bash

init_proxy_server() {
    if [[ -z ${PROXY_SERVER} ]]; then
        echo "未设置代理服务 \${PROXY_SERVER}"
    elif curl -o /dev/null -k -s -S -x ${PROXY_SERVER} --connect-timeout 5 https://github.com; then
        echo "使用代理服务器 \${PROXY_SERVER}:${PROXY_SERVER}"
        build_use_proxy="--build-arg ALL_PROXY=${PROXY_SERVER} \
      --build-arg HTTP_PROXY=${PROXY_SERVER} \
      --build-arg USE_PROXY=on \
      --build-arg all_proxy=${PROXY_SERVER} \
      --build-arg http_proxy=${PROXY_SERVER} \
      --build-arg use_proxy=on \
      --build-arg GO111MODULE=on \
      --build-arg GOPROXY=https://goproxy.io"
    else
        echo "请检查代理服务 \${PROXY_SERVER}:${PROXY_SERVER}"
    fi
}

PROXY_SERVER=$HTTP_PROXY_SERVER
Sourcepath=https://github.com/TechXueXi/TechXueXi.git
usebranche='dev'

init_proxy_server

docker build \
    ${build_use_proxy:-} \
    --build-arg Sourcepath=${Sourcepath} \
    --build-arg usebranche=${usebranche} \
    --tag techxuexi/techxuexi-amd64:${usebranche} \
    ${Sourcepath}