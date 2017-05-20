from ConfigParser import ConfigParser

class ThemeBuilderConfig(object):

    SECTION = 'Theme Builder'

    def __init__(self, path):
        self._config = ConfigParser()
        self._config.read(path)

    @property
    def prototype_path(self):
        return self._config.get(self.SECTION, 'prototype_path')

    @property
    def theme_path(self):
        return self._config.get(self.SECTION, 'theme_path')
