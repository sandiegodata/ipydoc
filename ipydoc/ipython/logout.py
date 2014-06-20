"""

Copyright (c) 2014 San Diego Regional Data Library. This file is licensed under the terms of the
Revised BSD License, included in this distribution as LICENSE.txt
"""

from IPython.html.base.handlers import IPythonHandler

class LogoutHandler(IPythonHandler):

    def send_logout_message(self):
        # Call the director service to create the container

        import os
        import zerorpc

        if not os.getenv('DIRECTOR_PORT') or not os.getenv('HOSTNAME'):
            self.log.info("Missing config for DIRECTOR_PORT or HOSTNAME; can't send logout message")
            return

        try:
            c = zerorpc.Client()
            c.connect(os.getenv('DIRECTOR_PORT'))
            c.logout(os.getenv('HOSTNAME'))
        except Exception as e:
            self.log.error("Failed to send logout message: {}".format(e))

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

##
## Monkey Patch the logout handler to shutdown the container
##

import IPython.html.auth.logout as logout

logout.default_handlers = [(r"/logout", LogoutHandler)]
