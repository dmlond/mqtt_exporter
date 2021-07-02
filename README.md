# MQTT Prometheus Exporter
python bridge between mqtt and prometheus

subscribes to a configurable set of mqtt queues,
and publishes the values to a Prometheus Scrape Target

## Build and Deploy

build.sh uses docker buildx to build an arm container image
and publish to a registry. Requires buildx and qemu.

## Delete

Deletes the image from the registry built by build.sh

## Deploy.sh

Publishes the helm chart

## Helm Chart

Publishes the mqtt_exporter to a kubernetes cluster with a service
annotated for prometheus autoscrape.