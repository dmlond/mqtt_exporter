#!/usr/local/bin/python
from prometheus_client import start_http_server, Gauge, Counter
import random
import time
import os
import signal
import paho.mqtt.client as mqtt
import yaml

required_environment = [
    'QUEUE_STREAM_FILE',
    'MQTT_USER',
    'MQTT_PASSWORD',
    'MQTT_HOST',
    'MQTT_PORT'
]
    
for required_key in required_environment:
    if required_key not in os.environ:
        print(f'missing required environment {required_key}')
        exit(1)

def exporter_for(exporter_type, exporter_key, exporter_summary):
    if exporter_type == 'Guage':
        return Gauge(exporter_key, exporter_summary)
    elif exporter_type == 'Counter':
        return Counter(exporter_key, exporter_summary)
    else:
      raise Exception(f'unsupported exporter type {exporter_type}')

queues = {}

def load_queues():
    if os.path.exists(os.environ['QUEUE_STREAM_FILE']):
        with open(os.environ['QUEUE_STREAM_FILE'], 'r') as queue_stream:
            queue_definitions = yaml.load(queue_stream, Loader=yaml.SafeLoader)
            for queue, spec in queue_definitions.items():
                queues[queue] = exporter_for(*spec)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for queue in queues.keys():
        client.subscribe(queue)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    queues[topic].set(payload)

client = mqtt.Client()

def reload(signum, frame):
    print('reloading config')
    client.loop_stop()
    run_main()

def run_main(**kwargs):
    # load_queus if present, then Start up the server to expose the metrics.
    load_queues()
    client.loop_start()

# load_queues on HUP
signal.signal(signal.SIGHUP, reload)

if __name__ == '__main__':
    client.username_pw_set(os.environ['MQTT_USER'],os.environ['MQTT_PASSWORD'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.environ['MQTT_HOST'],os.environ['MQTT_PORT'],60)
    start_http_server(8000)
    while True:
        run_main()