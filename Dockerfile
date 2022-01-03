FROM ubuntu:latest

# ========================
# Docker Image with 
# - Docker inside
# - Python 3.9 inside
# Target:
# - Image capable of using docker and python.
# ========================

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

WORKDIR /var/task/home

COPY pws /var/task/home/pws
COPY setup.py /var/task/home/setup.py

RUN python3 setup.py install

RUN mkdir /var/task/home/pws/plugins

ENTRYPOINT [ "python3", "-m", "pws.home.main", "--host", "0.0.0.0", "--port", "3000", "--plugins", "/var/task/home/pws/plugins", "--debug" ]