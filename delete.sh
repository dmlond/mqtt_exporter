#!/bin/bash

#https://serverfault.com/questions/895916/remove-docker-image-in-registry-by-removing-files-folders-on-server

if [ -z "${VERSION}" ]
then
  echo "ENV VERSION required" >&2
  exit 1
fi

resp=$(curl -s http://registry.k3s.iot/v2/mqtt_exporter/tags/list)
if echo "${resp}" | jq -r '.tags[] | select(. == "'${VERSION}'")' | grep ${VERSION}
then
  echo "will remove ${VERSION}"
  digest=$(curl -I  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" http://registry.k3s.iot/v2/mqtt_exporter/manifests/${VERSION} | grep 'Docker-Content-Digest' | cut -d' ' -f 2 | tr -d $'\r')
  curl -X DELETE "http://registry.k3s.iot/v2/mqtt_exporter/manifests/${digest}"
  curl -s http://registry.k3s.iot/v2/mqtt_exporter/tags/list
else
  echo "not present in ${resp}"
fi
