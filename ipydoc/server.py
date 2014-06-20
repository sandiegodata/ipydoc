"""ZeroRPC server for running the director

Copyright (c) 2014 San Diego Regional Data Library. This file is licensed under the terms of the
Revised BSD License, included in this distribution as LICENSE.txt
"""


import zerorpc
import argparse
import logging
from ipydoc import ProxyConfig, DockerClientRef
from manager import DockerManager, RedisManager, Director

class DockerServer(object):

    def __init__(self, director, logger):
        self.director = director
        self.logger = logger


    def version(self):
        """Return the version number"""
        import ipydoc
        return ipydoc.__version__

    def start(self, user, repo_url=None, github_auth=None):
        """Start an ipython container for a given user"""
        self.logger.info("Starting {}".format(user))
        r =  self.director.start(user, repo_url=repo_url, github_auth=github_auth)

        import time

        for i in range(45):
            if self.is_running(user):
                return r
            self.logger.info("Waiting for {} to start ".format(user))
            time.sleep(.25)

        self.logger.info("Gave up waiting for {} to start ".format(user))
        return False


    def stop(self, user):
        """Stop a user's Ipython container"""
        self.logger.info("Stopping {}".format(user))
        return self.director.stop(user)

    def start_dispatcher(self, host_id):
        """Set the proxy to point to the dispatcher"""
        self.logger.info("Start dispatcher at {}".format(host_id))
        return self.director.activate_dispatcher(host_id)

    def is_running(self, id):
        return self.director.is_running(id)

    def logout(self, host_id):
        """On logout, the IPython process on the container passes to us the whole environment"""
        import threading

        self.logger.info("Logging out {}".format(host_id))

        self.logger.info(host_id)

        self.director.logout(host_id)

        # Wait a few seconds to kill the container, so it can return a response to the
        # user.
        class WaitABit(threading.Thread):
            def run(this):
                import time
                time.sleep(5)
                self.logger.info("Killing {}".format(host_id))
                self.director.stop(host_id)


        t = WaitABit()
        t.start()


        return True



if __name__ == '__main__':
    import os
    import urlparse

    docker_connect =  os.getenv('DOCKER_HOST', 'tcp://0.0.0.0:4243')

    parser = argparse.ArgumentParser(description='Serve requests to start ipython containers',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--debug', action='store_true', help='turn on debugging')
    parser.add_argument('-p', '--port', type=int, default=4242, help='TCP Port to use')
    parser.add_argument('-H', '--host', default='0.0.0.0', type=str, help='Host IP address to attach to ')
    parser.add_argument('-D', '--docker', default= docker_connect,type=str, help='Connection URL to the docker host')

    parser.add_argument('-P', '--proxy-domain', type=str, required=True, help='Base domain for the proxy')
    parser.add_argument('-b', '--backend-host', type=str, help='Host address of the ipython containers, usually the docker host')
    parser.add_argument('-I', '--image', type=str, default='ipynb_ipython', help='Name of docker images for ipython container')

    parser.add_argument('-R', '--redis', type=str, required=True, help='Redis host')

    args = parser.parse_args()

    logger = logging.getLogger(__name__)

    if not args.backend_host:
        parts = urlparse.urlparse(args.docker)

        backend_host = parts.netloc.split(':')[0]
    else:
        backend_host = args.backend_host

    if args.debug:
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)

    redis_ = RedisManager(ProxyConfig(args.proxy_domain, backend_host), args.redis)

    docker = DockerManager(DockerClientRef(args.docker,'1.9', 10), args.image)

    d = Director(docker, redis_)

    docker_host = urlparse.urlparse(args.docker)[1].split(':',1)[0]

    s = zerorpc.Server(DockerServer(d, logger))
    s.bind("tcp://{}:{}".format(args.host, args.port))
    s.run()