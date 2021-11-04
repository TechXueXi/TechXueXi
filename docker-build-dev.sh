#!/bin/bash
# eg ./dev_build.sh https://github.com/TechXueXi/TechXueXi.git developing localhost:5000

USESOURCE='https://github.com/TechXueXi/TechXueXi.git'
USEBRANCHE='developing'
IMAGE_TAG="techxuexi/techxuexi-amd64:${USEBRANCHE}"
PUSH_REGISTRY_URL='docker.io'

if [[ $1 ]]; then
    USESOURCE=$1
fi
if [[ $2 ]]; then
    USESOURCE=$2
fi
if [[ $3 ]]; then
    PUSH_REGISTRY_URL=$3
    IMAGE_TAG=${PUSH_REGISTRY_URL}/${IMAGE_TAG}
fi

set -x
docker build \
    -f Dockerfile.dev \
    --build-arg "usesource=${USESOURCE}" \
    --build-arg "usebranche=${USEBRANCHE}" \
    --tag "${IMAGE_TAG}" \
    ${USESOURCE}

docker push
