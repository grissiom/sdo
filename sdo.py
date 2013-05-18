import serial

dev = None
logf = None

_procs = []

def sdo_write(data):
    if dev is not None:
        dev.write(data)
    return True

def sdo_wait_line(target):
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
        #print "cmp: (%s) vs (%s)" % (repr(line), repr(target))
    return False

def sdo_success(message):
    print '======='
    print  message
    print '======='
    return True

def sdo_fail(message):
    print '*******'
    print  message
    print '*******'
    return False

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

    def write(self, data):
        self._step.append(lambda p: sdo_write(data))

    def wait_line(self, data):
        self._step.append(lambda p: sdo_wait_line(data))

    def success(self, data):
        self._step.append(lambda p: sdo_success(data))

    def __call__(self):
        for s in self._step:
            if not s(self):
                return False
        return True
