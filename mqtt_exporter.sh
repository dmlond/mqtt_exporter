#!/bin/bash

${APP_HOME}/mqtt_exporter.py &
exporter_pid=$!
reload() {
  echo "reloading"
  kill -s HUP ${exporter_pid}
  ${APP_HOME}/mqtt_exporter.py
  exporter_pid=$!
}

trap reload SIGHUP

while true
do
  : # do nothing
done