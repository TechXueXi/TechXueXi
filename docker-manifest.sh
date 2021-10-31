#!/bin/bash


TAG='latest'
PUBLIC_REGISTRY_URL='docker.io'
PRIVATE_REGISTRY_URL='docker.io'
PUBLIC_COMMUNITY_USER='techxuexi'
PRIVATE_COMMUNITY_USER='techxuexi'
IMAGE_NAME='techxuexi'


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

if [[ $1 ]]; then
    PRIVATE_REGISTRY_URL=$1
fi

if [[ $2 ]]; then
    PRIVATE_COMMUNITY_USER=$2
fi

OUT_TAGS=""
for PLATFORM in amd64 arm64v8 arm32v7; do
    LOGGER_RUN docker pull --platform ${PLATFORM} ${PUBLIC_REGISTRY_URL}/${PUBLIC_COMMUNITY_USER}/${IMAGE_NAME}-${PLATFORM}:${TAG}
    OUT_TAGS="${OUT_TAGS} ${PUBLIC_REGISTRY_URL}/${PUBLIC_COMMUNITY_USER}/${IMAGE_NAME}-${PLATFORM}:${TAG}"
done

LOGGER_RUN docker manifest create ${PRIVATE_REGISTRY_URL}/${PRIVATE_COMMUNITY_USER}/${IMAGE_NAME}:${TAG} ${OUT_TAGS}

LOGGER_RUN docker manifest push ${PRIVATE_REGISTRY_URL}/${PRIVATE_COMMUNITY_USER}/${IMAGE_NAME}:${TAG}

LOGGER_RUN docker manifest inspect ${PRIVATE_REGISTRY_URL}/${PRIVATE_COMMUNITY_USER}/${IMAGE_NAME}:${TAG}

