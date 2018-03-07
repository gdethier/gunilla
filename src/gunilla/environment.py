import os
import configparser

from os.path import expanduser

class Environment(object):

    def __init__(self):
        self.debug = False
        self.force = False
        self.prototype_name = None
        self.prototype_template_path = None
        self.project_template_path = None

        self._try_read_environment_file()

    def _try_read_environment_file(self):
        home = expanduser("~")
        environment_file = os.path.join(home, '.gunillarc')

        if os.path.exists(environment_file):
            print("Reading environment from {}".format(environment_file))
            config = configparser.ConfigParser()
            config.read(environment_file)

            project_templates = config['project_templates'] if 'project_templates' in config else {}
            default_project_template = config['gunilla']['default_project_template'] if ('gunilla' in config) and ('default_project_template' in config['gunilla']) else ''
            if default_project_template in project_templates:
                self.project_template_path = project_templates[default_project_template]

            prototype_templates = config['prototype_templates'] if 'prototype_templates' in config else {}
            default_prototype_template = config['gunilla']['default_prototype_template'] if ('gunilla' in config) and ('default_prototype_template' in config['gunilla']) else ''
            if default_prototype_template in prototype_templates:
                self.prototype_template_path = prototype_templates[default_prototype_template]


_environment = Environment()


def instance():
    return _environment
