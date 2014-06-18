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

        import zerorpc

        c = zerorpc.Client()

        cn = "tcp://barker:49153"
        #cn = "tcp://localhost:4242"

        c.connect(cn)
        print c.version

        user = 'ericbusboom'

        repo = 'https://github.com/SDRDLAnalysts/testing.git'
        auth = 'a50fd9805127e87b0f6099bf75e480128180e795'

        c.stop(user)
        password = c.start(user, repo, auth)

        print password
