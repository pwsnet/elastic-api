FROM ubuntu:latest

# Image dependencies
# ========================

# Avoid TZ Prompt
ENV DEBIAN_FRONTEND noninteractive
# Update ubuntu
RUN apt-get update && apt-get dist-upgrade -y
# Install pip3
RUN apt-get install -y python3-pip

# Elastic API setup
# ========================

# Work directory
WORKDIR /var/task/elastic

# Copy Elastic API source
COPY pws /var/task/elastic/pws
# Copy Elastic API setup file
COPY setup.py /var/task/elastic/setup.py

# Install Elastic API
RUN python3 setup.py install

# Create the plugins directory
RUN mkdir -p /pws/plugins

ENTRYPOINT [ "python3", "-m", "pws.elastic.service", "--plugins", "/pws/plugins" ]