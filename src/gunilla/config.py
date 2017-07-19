_config = None

class Config(object):

    def __init__(self, data):
        self._data = data

    @property
    def project_name(self):
        return self._data["PROJECT_NAME"]

    def composer_dir_name(self):
        return "gunilla/" + self.project_name

    def composer_file_name(self):
        return self.composer_dir_name() + "/docker-compose.yml"

    def wordpress_container_name(self):
        return self.project_name + "_wordpress_1"


def _read_config():
    data = {}
    with open('gunilla.sh') as f:
        line = f.readline()
        while line:
            name, value = line.split('=')
            data[name] = value.strip(' \n\t"')
            line = f.readline()
    return Config(data)


def instance():
    global _config
    if not _config:
        _config = _read_config()
    return _config
