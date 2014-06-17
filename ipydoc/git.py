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

    def __init__(self,dir_, remote_url = None, username = None, password = None):
        import os
        import urlparse
      
        self.dir_ = dir_

        if self.dir_:

            if not os.path.exists(self.dir_):
                os.makedirs(self.dir_)

            self.saved_path = os.getcwd()
            try: os.chdir(self.dir_)
            except: self.saved_path = None
        else:
            self.saved_path = None

        self.remote_url = remote_url

        if username and password:
            self.auth = '{}:{}'.format(username, password)

        elif username:
            self.auth = username

        elif password:
            self.auth = password

        else:
            self.auth = None

        if self.auth:
            parts = list(urlparse.urlparse(self.remote_url))
            parts[1] = "{}@{}".format(self.auth, parts[1]) # urlparse is really horrible.
            self.remote_url = urlparse.urlunparse(parts)


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

    def clone(self):
        import os
        from ambry.dbexceptions import ConflictError

        if not self.remote_url:
            raise RepositoryException("Can't clone without setting remote_url in constructor")

        git.clone(self.remote_url, self.dir_)

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

        if not self.remote_url:
            raise RepositoryException("Can't push without setting remote_url in constructor")

        try:

            for line in git.push(self.remote_url,n=True, porcelain=True):
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
         
            
    def push(self):
        '''Push to  remote'''

        if not self.remote_url:
            raise RepositoryException("Can't push without setting remote_url in constructor")

        p =  git.push(self.remote_url)

        return True

    def pull(self):
        '''pull to  remote'''

        git.pull(self.remote_url)

        return True
