FROM ubuntu:jammy-20230308

RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y --fix-missing \
        curl \
        unzip \
        software-properties-common \
        vim \
        bind9-dnsutils \
        python3-pip \
        sshpass \
        netcat \
        git

RUN ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
#RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install --no-install-recommends -y \
    tzdata

RUN apt-get install -y \
    python3 python3-dev python3-venv python3-pip bluez \
    libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf \
    build-essential libopenjp2-7 libtiff5 libturbojpeg0-dev \
    ffmpeg liblapack3 liblapack-dev libatlas-base-dev

RUN mkdir -p /data/homeassistant/config

# Will handle setup post container
COPY script/bashrc ~/.bashrc

COPY requirements.txt /src/
RUN pip3 install -r /src/requirements.txt
COPY requirements_container.txt /src/
RUN pip3 install -r /src/requirements_container.txt

SHELL ["/bin/bash", "-c"]
