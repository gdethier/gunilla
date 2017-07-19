from gunilla.exceptions import ActionException
from gunilla.theme_builder.builder import ThemeBuilder
from gunilla.theme_builder.config import ThemeBuilderConfig
import os
import sys


def run_builder(root_path):
    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        raise ActionException("Provided path does not exist or is not a folder ({})".format(root_path))

    prototypes_path = os.path.join(root_path, 'prototypes')
    themes_path = os.path.join(root_path, 'themes')
    entries = os.listdir(prototypes_path)
    for entry in entries:
        prototype_path = os.path.join(prototypes_path, entry)
        if not os.path.isdir(prototype_path):
            continue

        print("Building prototype {}".format(entry))
        config_path = os.path.join(prototype_path, 'config')

        config = ThemeBuilderConfig(config_path)
        config.theme_path = os.path.join(themes_path, entry)

        prototype_dir = os.path.dirname(config_path)
        os.chdir(prototype_dir)

        builder = ThemeBuilder(config)
        builder.build()


def main():
    root_path = os.path.abspath(sys.argv[1])
    try:
        run_builder(root_path)
    except ActionException as e:
        print(e)
        sys.exit(-1)
