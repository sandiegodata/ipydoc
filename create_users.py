#!/usr/bin/env python 


# Run command: docker run -d -p 8567:8888 -v /proj/notebooks/user1:/notebooks ambry

import docker
from docker.client import APIError

image = 'ambry'
kill = True

users = [
    ('eric',8567),

]



client = docker.Client(base_url='tcp://192.168.1.30:4243',version='1.9',timeout=10)

containers = []

for (name, port) in users:
   
    

for (name, port) in users:
   
    

    

