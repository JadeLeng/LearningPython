class Chain(object):
    def __init__(self, path = 'GET'):
        self._path = path
        print (self._path, '__init__')
        #self._path = path


    def __getattr__(self, path):
        print (self._path, '__get__attr')
        return Chain('%s/%s' % (self._path, path))

    def __call__(self, path):
        print (self._path, '__call__')
        return Chain("%s/%s" % (self._path, path))

    def __str__(self):
        print (self._path, '__str__')
        return self._path

    __repr__ = __str__


Chain().users('Michael').group('student').repos
