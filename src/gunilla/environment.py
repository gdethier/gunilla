class Environment(object):

    def __init__(self):
        self._debug = False
        self._force = False

    @property
    def debug(self):
        return self._debug

    def enable_debug(self, enable):
        self._debug = enable

    @property
    def force(self):
        return self._force

    def enable_force(self, force):
        self._force = force


_environment = Environment()


def instance():
    return _environment
