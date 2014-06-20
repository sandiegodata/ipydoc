# iPython Notebook with per-user storage and config
# ESB: Added installation of ambry, but configuration left to another image. 

# Based on MAINTAINER Eduard Schaeli "eduard.schaeli@benthoo.ch"

# Based on crosbymichael/ipython
# Creates a Docker image with IPython Notebook installed.
#
# VERSION               0.0.1

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

RUN apt-get install -y openssh-server git-core libxml2-dev curl python 
RUN apt-get install -y build-essential make gcc python-dev wget libsqlite3-dev sqlite3
RUN apt-get install -y postgresql-client-9.1 postgresql-client-common libpq5
RUN apt-get install -y libpq-dev

RUN wget http://python-distribute.org/distribute_setup.py 
RUN python distribute_setup.py

RUN wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py 
RUN python get-pip.py

RUN apt-get install -y libfreetype6 libfreetype6-dev
RUN apt-get install -y python-imaging libpng-dev 
RUN apt-get install -y libzmq-dev
RUN apt-get install -y curl

# Needed to build matplotlib on ubuntu 14.04
RUN ln -s /usr/include/freetype2 /usr/include/freetype2/freetype

RUN pip install pyzmq
RUN pip install numpy
RUN pip install matplotlib
RUN pip install pandas
RUN pip install jinja2
RUN pip install ipython

RUN python -c "from IPython.external import mathjax; mathjax.install_mathjax()"

##
## Install Ambry
##

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/clarinova/ambry/master/support/install-ubuntu.sh)"
RUN ambry config install -f
RUN ambry library sync #kick2

# Do this after so the synced bundle databases are in the main libary, not in the cache.
COPY ambry.yaml /etc/ambry.yaml

##
## Configure IPython
##

RUN ipython profile create default
COPY ipython_notebook_config.py /.ipython/profile_default/ipython_notebook_config.py

RUN pip install 'git+https://github.com/sdrdl/ipydoc.git#egg=ipydoc' #change5

EXPOSE 8888
CMD ipython notebook  --ip=* --notebook-dir=/notebooks
