FROM ubuntu:14.04
MAINTAINER Ahmed Abdullah <ahmedaabdulwahed@gmail.com>

#install pre-requisites packages

RUN apt-get update && apt-get install -y apache2 git python-pip curl \
python python-dev python-distribute tar git curl nano wget dialog \
net-tools build-essential

# add pot services to container

ADD /pots /usr/pots
WORKDIR /usr/pots
RUN pip install .

EXPOSE 80

CMD python server.py
