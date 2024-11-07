#! /bin/bash

set -e
set -x

export NENO_VERSION=$(grep -Ei '^version = "(.+)"$' pyproject.toml | sed -E 's/version = "(.+)"/\1/')

echo "Building Docker image for Neno version $NENO_VERSION"

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

docker build --build-arg="NENO_VERSION=${NENO_VERSION}" -t neno:${NENO_VERSION}-huge .

docker tag neno:${NENO_VERSION}-huge $DOCKER_USERNAME/neno:${NENO_VERSION}-huge

docker push $DOCKER_USERNAME/neno:${NENO_VERSION}-huge
