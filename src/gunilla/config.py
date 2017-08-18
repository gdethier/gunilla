import json
_config = None

class Config(object):

    def __init__(self, data):
        self._data = data

    @property
    def project_name(self):
        return self._data["name"]

    def wordpress_container_name(self):
        return self.project_name + "_wordpress_1"

    @property
    def dependencies(self):
        return Dependencies(self._data["dependencies"])


class DictWrapper(object):

    def __init__(self, data):
        self._data = data

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        return self._data[key]


class Dependencies(DictWrapper):

    @property
    def plugins(self):
        if not 'plugins' in self._data:
            return ComponentDependencies({})
        return ComponentDependencies(self._data['plugins'])

    @property
    def themes(self):
        if not 'themes' in self._data:
            return ComponentDependencies({})
        return ComponentDependencies(self._data['themes'])


class ComponentDependencies(DictWrapper):

    def __getitem__(self, key):
        return Dependency(self._data[key])


class Dependency(DictWrapper):

    @property
    def version(self):
        return self._data["version"]


def _read_config():
    with open(config_file_path) as f:
        data = json.load(f)
    return Config(data)


config_file_path = 'gunilla.json'


def instance():
    global _config
    if not _config:
        _config = _read_config()
    return _config


def init_config_file():
    config_map = {}
    config_map["name"] = raw_input("Project name: ")
    with open(config_file_path, 'w') as f:
        json.dump(config_map, f, indent=4)
