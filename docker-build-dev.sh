#!/bin/bash
# eg ./docker-build-dev.sh https://github.com/TechXueXi/TechXueXi.git developing  localhost:5000 arm64v8 Dockerfile_arm64v8.dev

USESOURCE='https://github.com/TechXueXi/TechXueXi.git'
USEBRANCHE='developing'
IMAGE_TAG="techxuexi/techxuexi-amd64:${USEBRANCHE}"
PUSH_REGISTRY_URL='docker.io'
DOCKER_FILE='Dockerfile.dev'
if [[ $1 ]]; then
    USESOURCE=$1
fi
if [[ $2 ]]; then
    USEBRANCHE=$2
fi
if [[ $3 ]]; then
    PUSH_REGISTRY_URL=$3
    IMAGE_TAG=${PUSH_REGISTRY_URL}/${IMAGE_TAG}
fi
if [[ $4 ]]; then
    IMAGE_TAG="techxuexi/techxuexi-$4:${USEBRANCHE}"
fi
if [[ $5 ]]; then
    DOCKER_FILE=$5
fi
set -x
docker build \
    -f ${DOCKER_FILE} \
    --build-arg "usesource=${USESOURCE}" \
    --build-arg "usebranche=${USEBRANCHE}" \
    --tag "${IMAGE_TAG}" \
    .

docker push
