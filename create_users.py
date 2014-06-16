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
    container_name = 'ipy_'+name
    
    try:
        insp = client.inspect_container(container_name)
        if kill:
            container_id = insp['ID']
            
            if insp['State']['Running']:
                print "Killing {}".format(container_name)
                client.kill(container_id)
                
            client.remove_container(container_id)
            print "Removing {}".format(container_name)
        else:
            continue
    except APIError:
        pass
  
    cont = client.create_container(image, detach=True, name = container_name, 
                              ports = [8888], volumes = ['/notebooks'])
    
    # command=None, hostname=None, user=None,
    #               stdin_open=False, tty=False, mem_limit=0,
    #               ports=None, environment=None, dns=None, volumes=None,
    #               volumes_from=None, network_disabled=False, name=None,
    #               entrypoint=None, cpu_shares=None, working_dir=None,
    #               memswap_limit=0)
    

for (name, port) in users:
    container_name = 'ipy_'+name
    
    try:
        insp = client.inspect_container(container_name)
     
        if insp['State']['Running']:
            print 'Container {} is running'.format(container_name)
            
        else:
            print 'Starting {}'.format(container_name)
            
            external = '/proj/notebooks/{}/'.format(name)
            internal = '/notebooks'
            
            binds = { external :{
                        'bind': internal, 
                        'ro': False
                        } 
                    }
                    
            binds = {
                external: internal
            }
            
            client.start(insp['ID'],  port_bindings={8888:port}, binds = binds )
                    #lxc_conf=None,
                    #publish_all_ports=False, links=None, privileged=False,
                    #dns=None, dns_search=None, volumes_from=None, network_mode=None)
            
    except APIError as e:
        print e
        
    

    

