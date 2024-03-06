FROM ubuntu:jammy-20240227

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

# Setup non-root user
ARG USERNAME=homeassistant
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

# Create venv
ENV VENV=/home/${USERNAME}/venv
RUN python3 -m venv ${VENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Install packages for local development and home assistant
COPY --chown=${USER_UID}:${USER_GID} requirements.txt /home/${USERNAME}/
RUN pip install -r /home/${USERNAME}/requirements.txt

SHELL ["/bin/bash", "-c"]
