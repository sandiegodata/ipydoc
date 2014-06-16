ipython-docker
==============

Dockerfiles and scripts for running ipython 




Build the iptyhon image

  docker build -t ipython  https://raw.githubusercontent.com/clarinova/ipython-docker/master/Dockerfile-base-ipython

Build the ambry image

  docker build -t ambry  https://raw.githubusercontent.com/clarinova/ipython-docker/master/Docker-ambry

Runing an Ambry container

  docker run -d -p 8567:8888 -v  /proj/notebooks/user1:/notebooks ambry
