from gunilla.config import instance as config_instance
from gunilla.exceptions import ActionException
from gunilla.theme_builder.builder import ThemeBuilder
from gunilla.theme_builder.config import ThemeBuilderConfig
import os
import subprocess
import sys


def run_builder(root_path):
    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        raise ActionException("Provided path does not exist or is not a folder ({})".format(root_path))

    prototypes_path = os.path.join(root_path, 'prototypes')
    themes_path = os.path.join(root_path, 'themes')
    prototype_names = os.listdir(prototypes_path)
    for prototype_name in prototype_names:
        prototype_path = os.path.join(prototypes_path, prototype_name)
        if not os.path.isdir(prototype_path):
            continue

        gunilla_config = config_instance()
        prototype_config = gunilla_config.prototypes[prototype_name]
        prototype_root_path = os.path.join(prototypes_path, prototype_name)
        os.chdir(prototype_root_path)

        build_cmd = prototype_config.build_cmd
        if build_cmd:
            print("Building prototype {}".format(prototype_name))
            subprocess.call(["bash", "-c", build_cmd])

        print("Building theme {}".format(prototype_name))
        prototype_path = os.path.join(prototype_root_path, prototype_config.path)
        theme_path = os.path.join(themes_path, prototype_name)
        config = ThemeBuilderConfig(prototype_path, theme_path)

        builder = ThemeBuilder(config)
        builder.build()


def main():
    root_path = os.path.abspath(sys.argv[1])
    try:
        run_builder(root_path)
    except ActionException as e:
        print(e)
        sys.exit(-1)
