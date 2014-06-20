# Configuration file for ipython-notebook.

import os

c = get_config()

c.NotebookApp.cookie_secret =  os.getenv('IPYTHON_COOKIE_SECRET',  os.urandom(1024) )

# Fallback is 'foobar'
password = 'sha1:2d0d14557d41:e5c93b69dd5ca069a58f1c4a333d1c125ce4c4a5'
c.NotebookApp.password =  os.getenv('IPYTHON_PASSWORD', password )

c.NotebookApp.notebook_manager_class = 'ipydoc.ipython.manager.GitNotebookManager'

c.GitNotebookManager.repo_url = os.getenv('IPYTHON_REPO_URL')
c.GitNotebookManager.password = os.getenv('IPYTHON_REPO_AUTH')

c.NotebookApp.trust_xheaders=True

c.MappingKernelManager.time_to_dead=10
c.MappingKernelManager.first_beat=3

##
## Monkey Patch the logout handler to shutdown the container
##
from IPython.html.base.handlers import IPythonHandler

class LogoutHandler(IPythonHandler):

    def send_logout_message(self):
        # Call the director service to create the container

        import os
        import zerorpc

        c = zerorpc.Client()

        c.connect(os.getenv('DIRECTOR_PORT'))
        c.logout(os.getenv('HOSTNAME'))

    def get(self):
        import time

        self.clear_login_cookie()

        if self.login_available:
            message = {'info': 'Successfully logged out.'}
        else:
            message = {'warning': 'Cannot log out.  Notebook authentication '
                       'is disabled.'}

        self.send_logout_message()

        time.sleep(1) # Make sure the proxy has moved the entry for ths server

        self.redirect('/')

import IPython.html.auth.logout as logout

logout.default_handlers = [(r"/logout", LogoutHandler)]