from cherrypy import wsgiserver
import os
from os.path import dirname, join
import django.core.handlers.wsgi

import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipydispatch.settings")

    server = wsgiserver.CherryPyWSGIServer(
        ('0.0.0.0', 8000),
        django.core.handlers.wsgi.WSGIHandler(),
        server_name='localhost',
        numthreads = 20,
    )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()