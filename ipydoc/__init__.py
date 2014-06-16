"""Control a set of containers in docker for multi-user IPython Notebook

Copyright (c) 2014 San Diego Regional Data Library. This file is licensed under the terms of the
Revised BSD License, included in this distribution as LICENSE.txt
"""

__version__ = 0.01
__author__ = 'eric@sandiegodata.org'


class DockerClientRef(object):
    
    def __init__(self, url, version, timeout):
        self.url = url
        self.version = version
        self.timeout = timeout
        
        
    def open(self):
        import docker
        return docker.Client(self.url,self.version,self.timeout)


class ProxyConfig(object):

    def __init__(self, base_domain, common_ip, name_prefix='ipy-', base_port=8500):
        self.base_domain = base_domain.strip('.')
        self.common_ip = common_ip
        self.name_prefix =name_prefix
        self.base_port = base_port



