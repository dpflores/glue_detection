#arm64v8 is the pre-requisite for running the container on the VPU.
FROM ghcr.io/ifm/ifm3d:v0.93.0-ubuntu-arm64

# if you are running unit tests against a camera at
# a different IP, set it here.
# ENV IFM3D_IP 192.168.0.69




WORKDIR /home/ifm

#Security updates

ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive
# RUN sudo echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections

# RUN sudo apt-get update && sudo apt-get -y upgrade
# RUN apt-get update && \
#     apt-get install -y libboost-all-dev \
#                        git \
#                        libcurl4-openssl-dev \
#                        libgtest-dev \
#                        libgoogle-glog-dev \
#                        libxmlrpc-c++8-dev \
#                        libopencv-dev \
#                        libpcl-dev \
#                        libproj-dev \
#                        python3-dev \
#                        python3-pip

RUN sudo apt-get update

RUN sudo apt-get install -y git

RUN sudo apt-get install -y python3-pip

RUN sudo apt install -y libgl1-mesa-glx

RUN sudo apt-get install -y libglib2.0-0


# Adicional
# Para ver el hardware del sistema
RUN sudo apt-get install -y lshw



RUN sudo apt-get clean


# install python
# RUN apt-get -y install --no-install-recommends build-essential \
#     python3.8.10-dev

# Your normal pip installation, within the venv. We also update pip.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Add the repository to docker image
COPY --chown=ifm:ifm . /home/ifm/filling_detection


#For security reasons, using a "user" is recommended

USER ifm

#Easier to debug the container if issues are happening
ENV PYTHONFAULTHANDLER=1    