"""

@author: eric
"""
import unittest



class TestBase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestBase, self).__init__(methodName)

    def test_basic(self):
        import ipydoc
        from ipydoc.manager import DockerManager, RedisManager

        pc = ipydoc.ProxyConfig('ipy.clarinova.net', '192.168.1.30')

        redis = RedisManager(pc, 'hipache')

        cr = ipydoc.DockerClientRef('tcp://192.168.1.30:4243','1.9',10)

        m = DockerManager(cr,'ambry')

        user = 'binbat'

        c = m.create(user)

        c.start(redis.port_offset(user))

        redis.activate(user)


    def test_redis(self):
        import ipydoc
        from ipydoc.manager import RedisManager

        pc = ipydoc.ProxyConfig('ipy.clarinova.net', '192.168.1.30')

        redis = RedisManager(pc, 'hipache')



        redis.stub('bob')

        print redis.port_offset('sally')
