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

wait $exporter_pid
if [ $? -gt 0 ]
then
  echo "PROBLEM!" >&2
  exit 1
fi
