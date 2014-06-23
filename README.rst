ipydoc -- a Docker system for multi-user IPython 
==============

This is very alpha code for creating a network of Docker containers that will spawn an IPython container 
for each authorized user. 

Design Overview
-----------------------



Initial Setup
-----------------------




Building the Containers
-----------------------

Configuration
-------------

dispatcher
++++++++++


* DIRECTOR_PORT or --link ipynb_director:director

To run the dispatcher in test you can either run the development server, or run it with Cherrypi. In either case,
you'll have to fake the link to the director with an explicit environmental variable With cherrypi:

    HOSTNAME=29357b94a392 DIRECTOR_PORT=tcp://barker:49153  scripts/ipydoc_dispatch

Replace the value of 'barker:49153' with the hostname of Docker host and the port that the director maps to.
If you are running the director in development, the value will refer to the development instance, which is on port
4242, so you'll use a string like 'tcp://gala:4242'

The HOSTNAME should reference a dispatcher running in docker. The startup process will tell the director that
the dispatchers has started, so it can be sent a message when the user logs out of IPython. ( The HOSTNAME
variable is normally set by docker for the container; insite the container, the value references itself. ) You'll
can run any docker container to get this value, but when you click the "logout" button in IPython, the proxy will
use that host as the new backend for the ipython server you are one, so you will get an HTTP connection error after the
logout.

Or, with the development server.

    HOSTNAME=29357b94a392 DIRECTOR_PORT=tcp://barker:49153  scripts/ipydoc_manage runserver



director
++++++++

The director takes a lot of command line options, which you can get by  running:

    docker run --rm   ipynb_director -h

A typical invocation line will look like:

    docker run --rm  -t -i  -P --name ipynb_director ipynb_director  -I ipynb_ipython -P ipython.sandiegodata.org -R hipache  -D "tcp://barker:4243"


If you run the director in debugging, outside of docker,  you'll have to set the HOSTNAME to point to the host id of
a container, so the ipython container it creates can setup a link.

    HOSTNAME=ea12110b3d4f ipydoc_director -d  ....

One easy way to do this is:

    $ export HOSTNAME=$(docker run  -d -i busybox /bin/sh)
    $ ipydoc_director -d -I ipynb_ipython -P ipython.sandiegodata.org -R hipache  -D "tcp://barker:4243"

You can test that it is working with:

    $ zerorpc tcp://localhost:4242 version

Running the containers
----------------------

    $ docker run -d -t -i -v /data/ipynb/cache:/cache -v /data/ipynb/notebooks:/notebooks --name ipynb_volumes ipynb_volumes

    $ docker run -d -t -i  -P --name ipynb_director ipynb_director  -I ipynb_ipython -P ipython.sandiegodata.org -R hipache  -D "tcp://barker:4243"

    $ docker run -d -t -i  -P --link ipynb_director:director --name ipynb_dispatcher ipynb_dispatcher


Development Notes
-----------------

The django manage.py script is moved to scripts/ipydoc_manage

When working on the dispatcher and  running the server locally, you will have to comment out, in settings.py:

    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

Or, you will get an error about "Authentication failed: The redirect_uri MUST match the registered callback URL for this application."
