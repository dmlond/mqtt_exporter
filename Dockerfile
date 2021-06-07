FROM python:3.9.5-alpine

RUN mkdir -p /opt/app-root/src

WORKDIR /opt/app-root/src

ADD mqtt_exporter.py /opt/app-root/src/mqtt_exporter.py
ADD requirements.txt /opt/app-root/src/requirements.txt

RUN pip install -r requirements.txt && \
    chmod -R g=rwx /opt/app-root/src

CMD 'mqtt_exporter.py'