class ThemeBuilderConfig(object):

    def __init__(self, prototype_path, theme_path):
        self._prototype_path = prototype_path
        self._theme_path = theme_path

    @property
    def prototype_path(self):
        return self._prototype_path

    @property
    def theme_path(self):
        return self._theme_path
