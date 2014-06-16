"""git repository service

Copyright (c) 2013 Clarinova. This file is licensed under the terms of the
Revised BSD License, included in this distribution as LICENSE.txt
"""

from ambry.dbexceptions import ConfigurationError

from sh import git
from sh import ErrorReturnCode_1, ErrorReturnCode_128

from ambry.util import get_logger

import logging

global_logger = get_logger(__name__)
global_logger.setLevel(logging.FATAL)

class RepositoryException(Exception):
    pass

def walk(dir_):
    """Walk a directory tree and return a GitShellService for every
    repository"""
    import os

    for root, dirs, files in os.walk(dir_, topdown=False):

        if '.git' in dirs:
            dirs[:] = []

            yield GitShellService(root)



class GitShellService(object):
    '''Interact with Git services using the shell commands'''

    def __init__(self,dir_):
        import os
      
        self.dir_ = dir_

        if self.dir_:

            if not os.path.exists(self.dir_):
                os.makedirs(self.dir_)

            self.saved_path = os.getcwd()
            try: os.chdir(self.dir_)
            except: self.saved_path = None
        else:
            self.saved_path = None

    def __del__( self ): # Should be ContextManager, but not right model ... 
        import os
        if self.saved_path:
            os.chdir( self.saved_path )

    @property
    def path(self):
        return self.dir_

    def init(self):
        o = git.init()
        
        if o.exit_code != 0:
            raise RepositoryException("Failed to init git repo: {}".format(o))
        
        return True

    def init_remote(self, url):
        
        return git.remote('add','origin',url)

    def deinit(self):
        import os
        fn = os.path.join(self.dir_, '.gitignore')
        if os.path.exists(fn):
            os.remove(fn)
            
        dn = os.path.join(self.dir_, '.git')
        if os.path.exists(dn):
            from  ambry.util import rm_rf
            rm_rf(dn)
            
    def exists(self):
        import os
        return os.path.isdir(self.dir_)

    def initialized(self):
        import os
        return os.path.isdir(self.dir_) and os.path.isdir(os.path.join(self.dir_, '.git'))

    def add(self,path):
        import os
        from sh import pwd

        o = git.add(path)

        if o.exit_code != 0:
            raise RepositoryException("Failed to add file {} to  git repo: {}".format(path, o))
        
        return True        
  
    def stash(self):
        
        o = git.stash()
        
        if o.exit_code != 0:
            raise RepositoryException("Failed to stash in  git repo: {}".format( o))
        
        return True   
  
    def commit(self,message="."):
        
        try:
            git.commit(a=True, m=message)
        except ErrorReturnCode_1:
            pass

        return True  
     
    def needs_commit(self):
        import os
        
        try:
            for line in git.status(porcelain=True):
                if line.strip():
                    return True
      
            return False
        except ErrorReturnCode_128:
            global_logger.error("Needs_commit failed in {}".format(os.getcwd()))
            return False
    
    def needs_push(self):
        import os
        
        try:
            for line in git.push('origin','master',n=True, porcelain=True):
                if '[up to date]' in line:
                    return False
    
            return True
            
        except ErrorReturnCode_128:
            global_logger.error("Needs_push failed in {}".format(os.getcwd()))
            return False
     
    def needs_init(self):
        import os
        
        dot_git = os.path.join(os.getcwd(),'.git')
        return not (os.path.exists(dot_git) and os.path.isdir(dot_git))
           
    def ignore(self, pattern):
        import os
        
        fn = os.path.join(self.dir_,'.gitignore')
        
        if os.path.exists(fn):
            with open(fn,'rb') as f:
                lines = set([line.strip() for line in f])
        else:
            lines = set()
            
        lines.add(pattern)
        
        with open(fn,'wb') as f:
            for line in lines:
                f.write(line+'\n')      

    def char_to_line(self,line_proc):
        
        import StringIO
        sio = StringIO.StringIO('bingo')
        def _rcv(chr_,stdin):
            sio.write(chr_)
            if chr == '\n' or chr_ == ':':
                # This is a total hack, but there is no other way to detect when the line is
                # done being displayed that looking for the last character, which is not a \n
                if not sio.getvalue().endswith('http:') and not sio.getvalue().endswith('https:'):
                    line_proc(sio.getvalue(),stdin)
                    sio.truncate(0)
        return _rcv
         
            
    def push(self, username="Noone", password="None"):
        '''Push to  remote'''

        def line_proc(line,stdin):

            if "Username for" in line:
                stdin.put(username+ "\n")
                
            elif "Password for" in line:
                stdin.put(password+ "\n")

            else:
                print "git-push: ", line.strip()

        rcv = self.char_to_line(line_proc)

        
        try:
            # This is a super hack. See http://amoffat.github.io/sh/tutorials/2-interacting_with_processes.html
            # for some explaination. 
            p =  git.push('-u','origin','master',  _out=rcv,  _out_bufsize=0, _tty_in=True)
            p.exit_code
        except ErrorReturnCode_128:
            raise Exception("""Push to repository repository failed. You will need to store or cache credentials. 
            You can do this by using ssh, .netrc, or a credential maanger. 
            See: https://www.kernel.org/pub/software/scm/git/docs/gitcredentials.html""")
            
        return True

    def pull(self, username="Noone", password="None"):
        '''pull to  remote'''

        def line_proc(line,stdin):

            if "Username for" in line:
                stdin.put(username+ "\n")
                
            elif "Password for" in line:
                stdin.put(password+ "\n")

            else:
                print "git-push: ", line.strip()

        rcv = self.char_to_line(line_proc)

        
        try:
            # This is a super hack. See http://amoffat.github.io/sh/tutorials/2-interacting_with_processes.html
            # for some explaination. 
            p =  git.pull(  _out=rcv,  _out_bufsize=0, _tty_in=True)
            p.exit_code
        except ErrorReturnCode_128:
            raise Exception("""Push to repository repository failed. You will need to store or cache credentials. 
            You can do this by using ssh, .netrc, or a credential maanger. 
            See: https://www.kernel.org/pub/software/scm/git/docs/gitcredentials.html""")
            
        return True

    def clone(self,url,  dir_=None):
        import os
        from ambry.dbexceptions import ConflictError

        dir_ = self.dir_ if not dir_ else dir_

        git.clone(url,dir_)


class GitRepository(object):
    '''
    classdocs
    '''

    SUFFIX = '-ambry'

    def __init__(self,service, dir, **kwargs):
        
        self.service = service
        self.dir_ = dir # Needs to be 'dir' for **config, from yaml file, to work
        self._impl = None



    ##
    ## Only a few of the methods use self.service. They should be factored out
    ##

    @property
    def ident(self):
        '''Return an identifier for this service'''
        return self.service.ident


    def init_remote(self):
        self.bundle.log("Check existence of repository: {}".format(self.name))

        if not self.service.has(self.name):
            pass
            #raise ConfigurationError("Repo {} already exists. Checkout instead?".format(self.name))
            self.bundle.log("Creating repository: {}".format(self.name))
            self.service.create(self.name)

        self.impl.init_remote(self.service.repo_url(self.name))

    def delete_remote(self):

        if self.service.has(self.name):
            self.bundle.log("Deleting remote: {}".format(self.name))
            self.service.delete(self.name)

    ##
    ## Only a few methods use self.dir_
    ##

    @property
    def dir(self):
        '''The directory of ... '''
        return self.dir_





    @property
    def impl(self):
        if not self._impl:
            raise ConfigurationError("Must assign bundle to repostitory before this operation")

        return self._impl


    # ----

    def source_path(self, ident):
        '''Return the absolute directory for a bundle based on its identity'''
        import os

        return os.path.join(self.dir, ident.source_path)


    def init(self):
        '''Initialize the repository, both load and the upstream'''
        import os

        self.impl.deinit()

        self.impl.init()

        for p in ('*.pyc', 'build','.project','.pydevproject', 'meta/schema-revised.csv', 'meta/schema-old.csv'):
            self.impl.ignore(p)

        self.add('bundle.py')
        self.add('bundle.yaml')
        self.add('README.md')

        self.add('.gitignore')

        self.commit('Initial commit')

        
    def de_init(self):
        self.impl.deinit()
        
    
    def is_initialized(self):
        '''Return true if this repository has already been initialized'''
    

    def create_upstream(self): raise NotImplemented()
    
    def add(self, path):
        '''Add a file to the repository'''
        return self.impl.add(path)
    
    def commit(self, message):

        return self.impl.commit(message=message)
 
    def stash(self):
        return self.impl.stash()
    
    
    def needs_commit(self):
        return self.impl.needs_commit()
    
    def needs_push(self):
        return self.impl.needs_push()
    
    def needs_init(self):
        return self.impl.needs_init()
    
    def clone(self, url, path):
        '''Locate the source for the named bundle from the library and retrieve the 
        source '''
        import os

        d = os.path.join(self.dir, path)
       
        impl = GitShellService(None)

        impl.clone(url,d)
        
        return d
        
    def push(self, username="Noone", password="None"):
        '''Push any changes to the repository to the origin server'''

        return self.impl.push(username=username, password=password)
    
    def pull(self, username="Noone", password="None"):
        '''Pull any changes to the repository from the origin server'''
        return self.impl.pull(username=username, password=password)
    
    def register(self, library): 
        '''Register the source location with the library, and the library
        upstream'''
        raise NotImplemented()
    
    def ignore(self, path):  
        '''Ignore a file'''
        raise NotImplemented()
    



    def __str__(self):
        return "<GitRepository: account={}, dir={}".format(self.service, self.dir_)


class GitHubService(object):

    def __init__(self, user, password, org=None, **kwargs):
        self.org = org
        self.user = user
        self.password = password
        self.ident_url = 'https://github.com/'
        self.url = ur = 'https://api.github.com/'

        self.urls = {
            'repos': ur + 'orgs/{}/repos?page={{page}}'.format(
                self.org) if self.org else ur + 'users/{}/repos'.format(self.user),
            'deleterepo': ur + 'repos/{}/{{name}}'.format(self.org if self.org else self.user),
            'info': ur + 'repos/{}/{{name}}'.format(self.org),
            'repogit': ur + '{}/{{name}}.git'.format(self.org),
            'yaml': "https://raw.github.com/{}/{{name}}/master/bundle.yaml".format(self.org)
        }

        self.auth = (self.user, self.password)

    def get(self, url):
        '''Constructs a request, using auth is the user is set '''
        import requests, json

        if self.user:
            r = requests.get(url, auth=self.auth)
        else:
            r = requests.get(url)

        return r

    def has(self, name):
        import requests, json

        url = self.urls['info'].format(name=name)

        r = self.get(url)

        if r.status_code != 200:
            return False
        else:
            return True


    def create(self, name):
        '''Create a new upstream repository'''
        import requests, json

        payload = json.dumps({'name': name})
        r = requests.post(self.urls['repos'], data=payload, auth=self.auth)
        if r.status_code >= 300:
            raise Exception(r.headers)

        else:
            return r.json()

    def delete(self, name):
        '''Delete the upstream repository'''
        import requests, json

        r = requests.delete(self.urls['deleterepo'].format(name=name), auth=self.auth)

        if r.status_code != 204:
            raise Exception(r.headers)

        else:
            return True


    def list(self):
        import requests, yaml
        from ambry.util import OrderedDictYAMLLoader
        import pprint
        from yaml.scanner import ScannerError

        out = []

        for page in range(1, 500):
            url = self.urls['repos'].format(page=page)

            r = self.get(url)

            r.raise_for_status()

            for i, e in enumerate(r.json()):
                url = e['url'].replace('api.github.com/repos', 'raw.github.com') + '/master/bundle.yaml'
                r = requests.get(url)
                r.raise_for_status()
                try:
                    config = yaml.load(r.content, OrderedDictYAMLLoader)
                except ScannerError:
                    print r.content
                    raise
                ident = dict(config['identity'])
                ident['clone_url'] = e['clone_url']
                out.append(ident)

            if i < 29:  # WTF is this? Page limit?
                break

        return out

    def repo_url(self, name):

        return self.urls['repogit'].format(name=name).replace('api.github', 'github')

    @property
    def ident(self):
        '''Return an identifier for this service'''
        from urlparse import urlparse, urlunparse

        parts = list(urlparse(self.ident_url)[:])  # convert to normal tuple

        u = self.org if self.org else self.user

        parts[2] = parts[2] + u

        return urlunparse(parts)

    def __str__(self):
        return "<GitHubService: user={} org={}>".format(self.user, self.org)
