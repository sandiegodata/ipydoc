# Run the Django application ro login in users with Github and
# redirect to the ipython container

FROM ubuntu:13.04

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
RUN apt-get install -y  python python-dev python-pip

RUN pip install 'git+https://github.com/sdrdl/ipydoc.git#egg=ipydoc' #kicker4

RUN ipydoc_manage syncdb  --noinput

EXPOSE 8000

CMD ["ipydoc_dispatch"]