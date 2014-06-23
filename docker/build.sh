#!/bin/sh

##
## Go get some coffee; this will be a while
##

docker build -t ipynb_volumes volumes

docker build -t ipynb_director director

docker build -t ipynb_ipython ipython

docker build -t ipynb_dispatcher dispatcher

docker build -t ipynb_redis redis

docker build -t ipynb_hipache hipache