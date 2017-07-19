class Environment(object):

    def __init__(self):
        self._debug = False

    @property
    def debug(self):
        return self._debug

    def enable_debug(self, enable):
        self._debug = enable

_environment = Environment()

def instance():
    return _environment
