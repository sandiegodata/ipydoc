
from IPython.html.services.notebooks.filenbmanager import FileNotebookManager
from sh import git
from ..git import GitShellService
import os
from IPython.utils.traitlets import  Unicode

class GitNotebookManager(FileNotebookManager):


    repo_url = Unicode('foobar', config=True)
    username = Unicode('username', config=True)
    password = Unicode('password', config=True)

    def __init__(self, **kwargs):
        from sh import ErrorReturnCode_1, ErrorReturnCode_128

        r =  super(GitNotebookManager, self).__init__( **kwargs)

        if not self.repo_url:
            raise Exception("Didn't get a repo_url")

        self.gss = GitShellService(self.notebook_dir, self.repo_url, username=self.username, password=self.password)

        try:
            self.log.info("Cloning from {}".format(self.repo_url))
            self.gss.clone()
        except ErrorReturnCode_128 as e:
            self.log.info("Failed to clone; assuming b/c dir {} not empty: {}".format(self.notebook_dir, e))


    def save_notebook(self, model, name='', path=''):

        self.pull()

        model =  super(GitNotebookManager, self).save_notebook(model, name=name, path=path)

        os_path = self._get_os_path(model['name'], model['path'])

        self.commit_push(model)

        return model

    def update_notebook(self, model, name, path=''):

        self.pull()

        model =  super(GitNotebookManager, self).update_notebook(model, name=name, path=path)

        self.commit_push(model)

        return model

    def delete_notebook(self, name, path=''):
        self.pull()

        r = super(GitNotebookManager, self).delete_notebook(name=name, path=path)

        self.commit_push(None)

        return r

    def pull(self):

        self.log.info("Pulling notebooks dir")
        self.gss.pull()

    def commit_push(self, model):

        if model:
            f = (model['path']+'/'+model['name']).strip('/')
            self.log.info("Adding: {}".format(f))
            self.gss.add(f)

        self.log.info("Commit and push")

        self.gss.commit('Auto commit')

        self.gss.push()
