# Configuration file for ipython-notebook.

import os
from IPython.utils.traitlets import Bytes

c = get_config()
c.NotebookApp.cookie_secret =  os.getenv('IPYTHON_COOKIE_SECRET',  os.urandom(1024) )

password = 'sha1:2d0d14557d41:e5c93b69dd5ca069a58f1c4a333d1c125ce4c4a5'
c.NotebookApp.password =  os.getenv('IPYTHON_PASSWORD', password )

