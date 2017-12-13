class Environment(object):

    def __init__(self):
        self.debug = False
        self.force = False
        self.prototype_name = None
        self.prototype_template_path = None


_environment = Environment()


def instance():
    return _environment
