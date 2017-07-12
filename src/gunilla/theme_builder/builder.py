import os
import shutil

from gunilla.theme_builder.parser import HtmlParser


class ThemeBuilder(object):

    def __init__(self, config):
        self._config = config

    def build(self):
        print("Building theme with files from directory {}".format(os.path.abspath(self._config.prototype_path)))

        if os.path.exists(self._config.theme_path):
            shutil.rmtree(self._config.theme_path)
        os.makedirs(self._config.theme_path)

        entries = os.listdir(self._config.prototype_path)
        html_files = []
        for entry in entries:
            if entry.endswith('.html'):
                html_files.append(entry)
            elif os.path.isfile(os.path.join(self._config.prototype_path, entry)):
                shutil.copy(os.path.join(self._config.prototype_path, entry), os.path.join(self._config.theme_path, entry))
            elif os.path.isdir(os.path.join(self._config.prototype_path, entry)):
                shutil.copytree(os.path.join(self._config.prototype_path, entry), os.path.join(self._config.theme_path, entry))

        for html_file in html_files:
            print("Handling file {}".format(html_file))
            parser = HtmlParser(self._config, os.path.join(self._config.prototype_path, html_file))
            parser.parse()

        includes = os.listdir('includes')
        for include in includes:
            print("Copy {}".format(include))
            shutil.copy(os.path.join('includes', include), os.path.join(self._config.theme_path, include))
