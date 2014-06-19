#!/bin/sh

docker build -t ipynb_volumes volumes

docker build -t ipynb_director director

docker build -t ipynb_ipython ipython

