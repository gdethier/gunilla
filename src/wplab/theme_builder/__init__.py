import os
import sys
from wplab.theme_builder.builder import ThemeBuilder
from wplab.theme_builder.config import ThemeBuilderConfig


def main():
    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print "Provided config file does not exist {}".format(config_path)
        sys.exit(-1)

    config = ThemeBuilderConfig(config_path)
    prototype_dir = os.path.dirname(config_path)
    os.chdir(prototype_dir)

    builder = ThemeBuilder(config)
    builder.build()
