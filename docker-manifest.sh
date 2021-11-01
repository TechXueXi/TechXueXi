#!/bin/bash

# eg : ./docker-manifest.sh localhost:5000 dev79 youname
# 1. 拉取镜像         : docker pull docker.io/techxuexi/techxuexi-{}:dev79     % amd64 arm64v8 arm32v7
# 2. 推送镜像         : docker push localhost:5000/youname/techxuexi-{}:dev79   % amd64 arm64v8 arm32v7
# 3. 创建manifest    : docker docker manifest create MANIFEST_LIST MANIFEST [MANIFEST...]
# 4. 附加架构信息     ：docker manifest annotate [OPTIONS] MANIFEST_LIST MANIFEST
# 5. 推送manifest     ：docker manifest push  localhost:5000/youname/techxuexi:dev79
# 5. 显示manifest     ：docker manifest inspect localhost:5000/youname/techxuexi:dev79

TAG='latest'
PULL_REGISTRY_URL='docker.io'
PULL_COMMUNITY_USER='techxuexi'
IMAGE_NAME='techxuexi'
PUSH_REGISTRY_URL='docker.io'
PUSH_COMMUNITY_USER='techxuexi'

if [[ $1 ]]; then
  PUSH_REGISTRY_URL=$1
else
  PUSH_REGISTRY_URL=${PULL_REGISTRY_URL}
fi

if [[ $2 ]]; then
  TAG=$2
fi

if [[ $3 ]]; then
  PUSH_COMMUNITY_USER=$3
fi

LOG_INFO() {
  echo -e "\033[0;32m[INFO] $* \033[0m"
}
LOG_ERROR() {
  echo -e "\033[0;31m[ERROR] $* \033[0m"
}
LOG_WARNING() {
  echo -e "\033[0;33m[WARNING] $* \033[0m"
}

# 输出命令到日志并运行
LOGGER_RUN() {
  LOG_INFO "$*"
  bash -c "$*"
}

for ARCH in amd64 arm64v8 arm32v7; do

  case $ARCH in
  amd64)
    PLATFORM=x86_64
    ;;

  arm64v8)
    PLATFORM=arm64
    ;;

  arm32v7)
    PLATFORM=arm
    ;;
  esac

  LOGGER_RUN docker pull --platform ${PLATFORM} ${PULL_REGISTRY_URL}/${PULL_COMMUNITY_USER}/${IMAGE_NAME}-${ARCH}:${TAG}
  LOGGER_RUN docker tag ${PULL_REGISTRY_URL}/${PULL_COMMUNITY_USER}/${IMAGE_NAME}-${ARCH}:${TAG} ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}-${ARCH}:${TAG}
  LOGGER_RUN docker push ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}-${ARCH}:${TAG}
  OUT_TAGS="${OUT_TAGS} ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}-${ARCH}:${TAG}"
done
LOG_INFO # $ docker manifest create MANIFEST_LIST MANIFEST [MANIFEST...]
LOGGER_RUN docker manifest create ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG} ${OUT_TAGS}
if [ $? -ne 0 ]; then
  LOGGER_RUN docker manifest create --amend ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG} ${OUT_TAGS}
  echo "failed, retry"
fi
for ARCH in amd64 arm64v8 arm32v7; do

  case $ARCH in
  amd64)
    PLATFORM=x86_64
    ;;

  arm64v8)
    PLATFORM=arm64
    ;;

  arm32v7)
    PLATFORM=arm
    ;;
  esac

  LOG_INFO # $ docker manifest annotate [OPTIONS] MANIFEST_LIST MANIFEST
  LOG_INFO docker manifest annotate ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG} \
    ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}-${ARCH}:${TAG} \
    --os linux --arch ${PLATFORM}
done
LOG_INFO # $ docker manifest create MANIFEST_LIST MANIFEST [MANIFEST...]
LOGGER_RUN docker manifest create ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG} ${OUT_TAGS}
if [ $? -ne 0 ]; then
  LOGGER_RUN docker manifest create --amend ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG} ${OUT_TAGS}
  echo "failed, retry"
fi

LOGGER_RUN docker manifest push ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG}

LOGGER_RUN docker manifest inspect ${PUSH_REGISTRY_URL}/${PUSH_COMMUNITY_USER}/${IMAGE_NAME}:${TAG}
