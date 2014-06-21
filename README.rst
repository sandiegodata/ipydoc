ipython-docker
==============

Dockerfiles and scripts for running ipython 


Building the Containers
-----------------------

Configuration
-------------

dispatcher
++++++++++

* DIRECTOR_PORT or --link ipynb_director:director

To run the dispatcher in test you can either run the development server, or run it with Cherrypi. With cherrypi:

    HOSTNAME=29357b94a392 DIRECTOR_PORT=tcp://barker:49153  scripts/ipydoc_dispatch

The HOSTNAME should reference a dispatcher running in docker. The startup process will tell the director that
the dispatchers has started, so it can be sent a message when the user logs out of IPython.

Or, with the development server.

    scripts/ipydoc_manage runserver


director
++++++++

Run the director from the command line, and connect the dispatcher to it with an env var:

    docker run --rm -t -i  -P  -e 'DIRECTOR_PORT=tcp://gala:4242' --name ipynb_dispatcher ipynb_dispatcher

* HOSTNAME env var.

If you run thedirector in dugging, you'll have to set the HOSTNAME to point to the host id of
a container, so the ipython container it creates can setup a link.

    HOSTNAME=ea12110b3d4f ipydoc_director -d  ....


Running the containers
----------------------

    $ docker run -d -t -i -v /data/ipynb/cache:/cache -v /data/ipynb/notebooks:/notebooks --name ipynb_volumes ipynb_volumes

    $ docker run -d -t -i  -P --name ipynb_director ipynb_director  -I ipynb_ipython -P ipython.sandiegodata.org -R hipache  -D "tcp://barker:4243"

    $ docker run -d -t -i  -P --link ipynb_director:director --name ipynb_dispatcher ipynb_dispatcher


Development Notes
-----------------

The django manage.py script is moved to scripts/ipydoc_manage