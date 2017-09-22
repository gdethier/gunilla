from gunilla.exceptions import ConfigException
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

    @property
    def prototypes(self):
        return Prototypes(self._data["prototypes"])


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


class DependencyType(object):
    DOWNLOAD = "download"
    FOLDER = "folder"


class Dependency(DictWrapper):

    @property
    def type(self):
        if "type" in self._data:
            return self._wrap_type(self._data["type"])
        else:
            return DependencyType.DOWNLOAD

    def _wrap_type(self, type_string):
        if type_string == DependencyType.DOWNLOAD:
            return DependencyType.DOWNLOAD
        elif type_string == DependencyType.FOLDER:
            return DependencyType.FOLDER
        else:
            raise ConfigException("Unsupported dependency type " + type_string)

    @property
    def version(self):
        return self._data["version"]


class Prototypes(DictWrapper):
    def __getitem__(self, key):
        return Prototype(self._data[key])


class Prototype(DictWrapper):

    @property
    def path(self):
        return self._data['path']

    @property
    def build_cmd(self):
        if 'build_cmd' in self._data:
            return self._data['build_cmd']
        else:
            return ''


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
