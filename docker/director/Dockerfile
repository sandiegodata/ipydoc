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

RUN apt-get install -y python-pip git

RUN pip install 'git+https://github.com/sdrdl/ipydoc.git#egg=ipydoc'

EXPOSE 4242

#CMD ["-d", "-P ipython.sandiegodata.org" "-R hipache"]

#ENTRYPOINT ["python -mipydoc.server"]

