import os
import shutil

from wplab.theme_builder.parser import HtmlParser


class ThemeBuilder(object):

    def __init__(self, config):
        self._config = config

    def build(self):
        print("Building theme with files from directory {}".format(os.path.abspath(self._config.prototype_path)))
        entries = os.listdir(self._config.prototype_path)
        html_files = []
        for entry in entries:
            if entry.endswith('.html'):
                html_files.append(entry)

        if not os.path.exists(self._config.theme_path):
            os.makedirs(self._config.theme_path)

        for html_file in html_files:
            print("Handling file {}".format(html_file))
            parser = HtmlParser(self._config, os.path.join(self._config.prototype_path, html_file))
            parser.parse()

        includes = os.listdir('includes')
        for include in includes:
            print("Copy {}".format(include))
            shutil.copy(os.path.join('includes', include), os.path.join(self._config.theme_path, include))
