FROM ubuntu:jammy-20230308

RUN apt-get update --fix-missing && \
    apt-get upgrade -y
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

#RUN apt-get install -y \
#   python3 python3-dev python3-venv python3-pip bluez \
#    libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf \
#    build-essential libopenjp2-7 libtiff5 libturbojpeg0-dev \
#    tzdata ffmpeg liblapack3 liblapack-dev libatlas-base-dev
#
#RUN pip3 install -r /workspaces/homeassistant-minecraft-profile/requirements_container.txt

# Create the virtual environment
#RUN useradd -rm homeassistant -G dialout,gpio,i2c
#RUN mkdir /data/homeassistant
#RUN chown homeassistant:homeassistant /data/homeassistant
#RUN ln -s /data/homeassistant/custom_components/ /workspaces/homeassistant-minecraft-profile/custom_components/

COPY requirements.txt /src/
RUN pip3 install -r /src/requirements.txt && \
    rm -fr /src

SHELL ["/bin/bash", "-c"]
