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


RUN sudo apt-get update

RUN sudo apt-get install -y vim

RUN sudo apt-get install -y python3-pip

# Para Opencv
RUN sudo apt install -y libgl1-mesa-glx

RUN sudo apt-get install -y libglib2.0-0


# Adicional
# para el candump
RUN sudo apt-get install can-utils


RUN sudo apt-get clean

# Your normal pip installation, within the venv. We also update pip.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Add the repository to docker image
COPY --chown=ifm:ifm ./can_opencv /home/ifm/application


#For security reasons, using a "user" is recommended

USER ifm

#Easier to debug the container if issues are happening
ENV PYTHONFAULTHANDLER=1 


# Para el jupyter notebook
EXPOSE 8888

# Startup
ENTRYPOINT ["jupyter", "notebook"]


