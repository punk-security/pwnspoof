FROM python:alpine

COPY ./* /app/

WORKDIR /app/

RUN mkdir /output/

ENTRYPOINT [ "/app/docker_start.sh" ]