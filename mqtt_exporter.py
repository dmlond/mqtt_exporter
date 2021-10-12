#!/usr/local/bin/python
from prometheus_client import start_http_server, Gauge, Counter
import os
import paho.mqtt.client as mqtt
import json

required_environment = [
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

register_queue = 'exporter/register'
queues = {}

def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print(f'subscribing to {register_queue}')
    client.subscribe(register_queue)
    for queue in queues.keys():
        print(f'subscribing to {queue}')
        client.subscribe(queue)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload

    if topic == register_queue:
        print(f'registering {payload}')
        queue_definition = json.loads(payload)
        for queue, spec in queue_definition.items():
            if queue not in queues:
                print(f'creating {spec} for {queue}')
                queues[queue] = [
                    exporter_for(*spec),
                    exporter_for('Guage', spec[1]+"_ping", spec[1]+" ping time")
                ]
    else:
        print(f'publishing {topic} metric {payload}')
        queues[topic][0].set(payload)
        queues[topic][1].set_to_current_time()

client = mqtt.Client()

if __name__ == '__main__':
    if 'MQTT_USER' in os.environ:
      client.username_pw_set(os.environ['MQTT_USER'],os.environ['MQTT_PASSWORD'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.environ['MQTT_HOST'],int(os.environ['MQTT_PORT']),60)

    start_http_server(8000)
    client.loop_forever()