"""

@author: eric
"""
import unittest
import os

def rm_rf( d):
    """Recursively delete a directory"""

    if not os.path.exists(d):
        return

    for path in (os.path.join(d,f) for f in os.listdir(d)):
        if os.path.isdir(path):
            rm_rf(path)
        else:
            os.unlink(path)
    os.rmdir(d)

class TestBase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestBase, self).__init__(methodName)

    def test_basic(self):

        from ipydoc.git import GitShellService
        import os
        import uuid

        directory = '/tmp/gittest'
        repo_url = 'https://github.com/sdrdl/SDRDL-Internship-Notebooks.git'

        #rm_rf(directory)

        css = GitShellService(directory, repo_url, 'a50fd9805127e87b0f6099bf75e480128180e795' )

        if css.initialized():
            print "Pulled"
            css.pull()
        else:
            print "Cloned"

            css.clone()

        u = uuid.uuid4()

        fn = os.path.join(directory, 'uuid')

        with open(fn, 'w+') as f:
            f.write(str(u))

        print 'Wrote', str(u)

        css.add('uuid')

        print 'Needs Commit', css.needs_commit()

        css.commit('Updated {} in testing'.format(str(u)))

        print 'Needs Commit', css.needs_commit()

        print 'Needs Push', css.needs_push()

        css.push()

        print 'Needs Push', css.needs_push()
