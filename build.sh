#!/bin/bash
#https://www.starkandwayne.com/blog/building-docker-images-for-kubernetes-on-arm/
if [ -z "${VERSION}" ]
then
  echo "ENV VERSION required" >&2
  exit 1
fi

docker buildx build --platform linux/arm/v7 -o type=registry,registry.insecure=true -t registry.k3s.iot/mqtt_exporter:${VERSION} .
echo "built mqtt_exporter.${VERSION}.tar"
