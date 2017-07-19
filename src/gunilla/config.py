import json
_config = None

class Config(object):

    def __init__(self, data):
        self._data = data

    @property
    def project_name(self):
        return self._data["name"]

    def composer_dir_name(self):
        return "gunilla/" + self.project_name

    def composer_file_name(self):
        return self.composer_dir_name() + "/docker-compose.yml"

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
        return ComponentDependencies(self._data["plugins"])

    @property
    def themes(self):
        return ComponentDependencies(self._data["themes"])


class ComponentDependencies(DictWrapper):

    def __getitem__(self, key):
        return Dependency(self._data[key])


class Dependency(DictWrapper):

    @property
    def version(self):
        return self._data["version"]


def _read_config():
    with open('gunilla.json') as f:
        data = json.load(f)
    return Config(data)


def instance():
    global _config
    if not _config:
        _config = _read_config()
    return _config
