#
# VERSION               0.0.1

FROM ubuntu:14.04

MAINTAINER Eric Busboom "eric@clarinova.com"

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y language-pack-en
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

RUN apt-get install -y build-essential make gcc wget curl git
RUN apt-get install -y python python-pip python-dev

RUN pip install 'git+https://github.com/sdrdl/ipydoc.git#egg=ipydoc' # change6

EXPOSE 4242

ENTRYPOINT ["ipydoc_director"]



