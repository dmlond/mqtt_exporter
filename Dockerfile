FROM python:3.9.5-alpine

ENV APP_HOME /opt/app-root/src

RUN mkdir -p ${APP_HOME}

WORKDIR ${APP_HOME}

ADD mqtt_exporter.py ${APP_HOME}/mqtt_exporter.py
ADD mqtt_exporter.sh ${APP_HOME}/mqtt_exporter.sh
ADD requirements.txt ${APP_HOME}/requirements.txt

RUN pip install -r requirements.txt && \
    chmod -R g=rwx ${APP_HOME}

CMD "${APP_HOME}/mqtt_exporter.sh"