# Configuration file for ipython-notebook.

import os

c = get_config()

c.NotebookApp.cookie_secret =  os.getenv('IPYTHON_COOKIE_SECRET',  os.urandom(1024) )
c.NotebookApp.password =  os.getenv('IPYTHON_PASSWORD')
c.NotebookApp.notebook_manager_class = 'ipydoc.ipython.manager.GitNotebookManager'
c.NotebookApp.notebook_dir = os.path.join('/notebooks',os.getenv('GITHUB_USER', 'unknown_user'))

if not os.path.exists(c.NotebookApp.notebook_dir):
    os.makedirs(c.NotebookApp.notebook_dir)

c.GitNotebookManager.repo_url = os.getenv('IPYTHON_REPO_URL')
c.GitNotebookManager.password = os.getenv('IPYTHON_REPO_AUTH')
c.GitNotebookManager.email = os.getenv('GITHUB_EMAIL', 'unset@sandiegodata.org')
c.GitNotebookManager.name = os.getenv('GITHUB_NAME', 'Unbuntu Nset')

c.NotebookApp.trust_xheaders=True

c.MappingKernelManager.time_to_dead=10
c.MappingKernelManager.first_beat=3

##
## Monkey Patch the logout handler to shutdown the container
##

import ipydoc.ipython.logout