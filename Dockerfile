# Python and Linux Version 
ARG EnvironmentVariable
FROM python:3.10.6-slim

# ENTRYPOINT command param1 param2

# setup environment variable  
# ENV DockerHOME=/home/app/webapp  

# set work directory  
# RUN mkdir -p $DockerHOME  

COPY requirements.txt /app/requirements.txt
# COPY requirements.txt /requirements.txt


ENV PYTHONUNBUFFERED=1

# Add unstable repo to allow us to access latest GDAL builds
# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
RUN echo deb http://deb.debian.org/debian testing main contrib non-free >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get remove -y binutils && \
    apt-get autoremove -y 

# RUN apk update && apk add build-base python3-dev libffi-dev openssl-dev && pip3 install magic-wormhole
RUN DEBIAN_FRONTEND="noninteractive" apt-get install libmagickwand-dev --no-install-recommends -y

# Install GDAL dependencies
# RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
#     pip install pipenv && \
#     pip install whitenoise && \
#     pip install gunicorn && \
#     apt-get clean -y

RUN pip install --no-cache-dir -r /app/requirements.txt 
# RUN pip install --no-cache-dir -r /requirements.txt 


# Update C env vars so compiler can find gdal
# ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"

WORKDIR /app

ADD . .

# EXPOSE 6226
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000