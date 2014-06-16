# iPython Notebook with per-user storage and config
# ESB: Added installation of ambry, but configuration left to another image. 

# Based on MAINTAINER Eduard Schaeli "eduard.schaeli@benthoo.ch"

# Based on crosbymichael/ipython
# Creates a Docker image with IPython Notebook installed.
#
# It expects to be run like this: 
#
# docker run -v /home/eduard/notebooks/eduard:/notebooks benthoo/ipython-user
#
# You provide a folder per user on the host system. This folder will hold the users notebooks and also needs to contain the
# ipython config file (ipython_notebook_config.py). There you can configure a password, which should be unique for each user.
#
# This way, you can run an instance of IPython per user, while each user has separate storage on the host machine and an
# individual password.
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

RUN pip install pyzmq
RUN pip install numpy
RUN pip install matplotlib
RUN pip install pandas
RUN pip install jinja2
RUN pip install ipython
RUN python -c "from IPython.external import mathjax; mathjax.install_mathjax()"

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/clarinova/ambry/master/support/install-ubuntu.sh)"

VOLUME /notebooks

# Create the default profile structure and replace the config file with a symlink to the one in the users folder.
# This way, each user can have his own config and the password can be set individually.
RUN ipython profile create default
COPY ipython_notebook_config.py /.ipython/profile_default/ipython_notebook_config.py

EXPOSE 8888

CMD ipython notebook  --ip=* --MappingKernelManager.time_to_dead=10 --MappingKernelManager.first_beat=3 \
    --notebook-dir=/notebooks  --NotebookApp.trust_xheaders=True
