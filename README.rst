ipython-docker
==============

Dockerfiles and scripts for running ipython 


Building the Containers
-----------------------


Running the containers
----------------------

    $ docker run -d -t -i -v /data/ipynb/cache:/cache -v /data/ipynb/notebooks:/notebooks --name ipynb_volumes ipynb_volumes

    $ docker run -d -t -i  -P --name ipynb_director ipynb_director  -I ipynb_ipython -P ipython.sandiegodata.org -R hipache  -D "tcp://barker:4243"

    $ docker run -d -t -i  -P --link ipynb_director:director --name ipynb_dispatcher ipynb_dispatcher