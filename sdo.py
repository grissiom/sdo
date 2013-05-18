dev = None
logf = None

_procs = []

def loop(loop_time):
    for i in xrange(loop_time):
        print 'start loop %d' % i
        for p in _procs:
            if not p():
                print 'failed at loop %d' % i
        print 'finish loop %d' % i

class proc(object):
    def __init__(self):
        _procs.append(self)
        self._step = []

    def _expose_closure(func):
        def _func(self, data):
            self._step.append(lambda : func(self, data))
        return _func

    @_expose_closure
    def write(self, data):
        if dev is not None:
            dev.write(data)
        return True

    @_expose_closure
    def wait_line(self, target):
        line = ''
        while True:
            c = dev.read(1)
            if logf is not None:
                logf.write(c)
            if c == '\n':
                if line[-1] == '\r':
                    line = line[:-1]
                if line == target:
                    return True
                else:
                    line = ''
            else:
                line += c
        return False

    @_expose_closure
    def success(self, message):
        print '======='
        print  message
        print '======='
        return True

    @_expose_closure
    def fail(self, message):
        print '*******'
        print  message
        print '*******'
        return False

    def __call__(self):
        for s in self._step:
            if not s():
                return False
        return True
