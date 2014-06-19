ipython-docker
==============

Dockerfiles and scripts for running ipython 


Building the Containers
-----------------------

Build the iptyhon image

  docker build -t ipython  https://raw.githubusercontent.com/clarinova/ipython-docker/master/Dockerfile-base-ipython

Build the ambry image

  docker build -t ambry  https://raw.githubusercontent.com/clarinova/ipython-docker/master/Docker-ambry

Runing an Ambry container

  docker run -d -p 8567:8888 -v  /proj/notebooks/user1:/notebooks ambry


Running the containers
----------------------

    $ docker run -d -t -i -v /data/ipynb/cache:/cache -v /data/ipynb/notebooks:/notebooks --name ipynb_volumes ipynb_volumes

    $ docker run -d -t -i  -P --name ipynb_director ipynb_director  -I ipynb_ipython -P ipython.sandiegodata.org -R hipache  -D "tcp://barker:4243"

