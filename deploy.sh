#!/bin/bash

if [ -z "${VERSION}" ]
then
  echo "ENV VERSION required" >&2
  exit 1
fi

helm upgrade mqtt-exporter-${VERSION} helm_chart/mqtt-exporter \
  --atomic --reset-values --debug --wait --timeout "${TIMEOUT:-1m30s}" --install \
  --set-string mqttExporter.tag=$VERSION \
  ${CONFIG_FILE:+ --set-file mqttExporter.configFile=$CONFIG_FILE}