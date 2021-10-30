PROXY_SERVER="http://192.168.168.121:21086"

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

TAG='Alpha'
Sourcepath=https://github.com/nineja5340/TechXueXi.git
docker build \
    ${build_use_proxy:-} \
    --build-arg Sourcepath=${Sourcepath} \
    --shm-size 2g \
    --tag techxuexi/techxuexi-amd64:${TAG:-'dev'} \
    https://github.com/nineja5340/TechXueXi.git
