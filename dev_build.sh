PROXY_SERVER="HTTP://192.168.168.121:21086"

if [[ -z ${PROXY_SERVER} ]]; then
    echo "未设置代理服务 \${PROXY_SERVER}"
elif curl -k -sS -x ${PROXY_SERVER} --connect-timeout 5 https://github.com; then
    echo "使用代理服务器 \${PROXY_SERVER}:${PROXY_SERVER}"
    build_cmd="--build-arg ALL_PROXY=${PROXY_SERVER} \
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

# ${ varname :- word } ：如果varname存在并且不为null，返回varname的值，否则返回word。

TAG='Alpha'

docker build \
    \ # --platform=linux/amd64,linux/arm64,linux/arm/v7
    ${build_cmd:-} \
    --tag techxuexi/techxuexi-amd64${TAG:-:TAG}
