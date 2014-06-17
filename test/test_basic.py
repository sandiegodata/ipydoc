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
        import ipydoc
        from ipydoc.manager import DockerManager, RedisManager, Director

        redis = RedisManager(ipydoc.ProxyConfig('ipython.sandiegodata.org', '192.168.1.30'),
                             'hipache')

        docker = DockerManager(ipydoc.DockerClientRef('tcp://192.168.1.30:4243','1.9',10),'ipython')

        d = Director(docker, redis)

        user = 'ericbusboom'

        #d.stop(user)

        repo = 'https://github.com/SDRDLAnalysts/testing.git'
        auth = 'a50fd9805127e87b0f6099bf75e480128180e795'

        password = d.start(user, repo, auth)

        print 'Password', password



    def test_redis(self):
        import ipydoc
        from ipydoc.manager import RedisManager

        pc = ipydoc.ProxyConfig('ipy.clarinova.net', '192.168.1.30')

        redis = RedisManager(pc, 'hipache')


        redis.stub('bob')

        print redis.port_offset('sally')


    def test_git(self):

        from ipydoc.git import GitShellService
        import os
        import uuid

        directory = '/tmp/gittest'
        repo_url = 'https://github.com/sdrdl/SDRDL-Internship-Notebooks.git'

        rm_rf(directory)

        css = GitShellService(directory)

        if css.initialized():
            print "Pulled"
            css.pull()
        else:
            print "Cloned"
            css.clone(repo_url)

        u = uuid.uuid4()

        fn = os.path.join(directory, 'uuid')

        with open(fn, 'w+') as f:
            f.write(str(u))

        print 'Wrote', str(u)

        css.add('uuid')

        print 'Needs Commit', css.needs_commit()

        css.commit('Updated {} in testing'.format(str(u)))

        print 'Needs Push', css.needs_push()

        css.push()

    def test_walk(self):

        from ipydoc.git import walk

        root = '/Users/eric/proj'

        for i, gss in enumerate(walk(root)):

            if i > 5: break

            print gss.needs_commit(), gss.path


    def test_watch(self):

        import watchdog
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        from ipydoc.git import walk

        from ipydoc import LockedSet

        root = '/tmp/gitwatch'


        class EventHandler(FileSystemEventHandler):

            def __init__(self, gss, ls ):
                self.gss = gss
                self.ls = ls

            def on_any_event(self, event):
                print self.gss.path, event

                self.ls.add(self.gss.path)

        locked_set = LockedSet()

        observer = Observer()
        for i, gss in enumerate(walk(root)):

            if i > 10: break

            print 'Scheduling', gss.path
            observer.schedule( EventHandler(gss, locked_set), gss.path, recursive = True)

        observer.start()

        try:
            import time
            while True:
                time.sleep(1)
                print locked_set
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

