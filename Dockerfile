FROM ubuntu:latest

# Image dependencies
# ========================

# Avoid TZ Prompt
ENV DEBIAN_FRONTEND noninteractive
# Update ubuntu
RUN apt-get update && apt-get dist-upgrade -y
# Install pip3
RUN apt-get install -y python3-pip

# PWS Home Base
# ========================

WORKDIR /var/task/elastic

COPY pws /var/task/elastic/pws
COPY setup.py /var/task/elastic/setup.py

RUN python3 setup.py install

RUN mkdir /pws/plugins

ENTRYPOINT [ "python3", "-m", "pws.elastic.main", "--plugins", "/pws/plugins" ]