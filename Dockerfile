FROM python:alpine

COPY *.py /app/

COPY IP2LOCATION-LITE-DB1.CSV /app/

COPY docker_start.sh /app/

WORKDIR /app/

RUN mkdir /output/

ENTRYPOINT [ "/app/docker_start.sh" ]