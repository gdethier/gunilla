import os
import argparse
import configparser

from os.path import expanduser
from gunilla.exceptions import ActionException

class Environment(object):

    def __init__(self):
        self._parser = self._build_arg_parser()

        self.action = None
        self.debug = False
        self.force = False
        self.workspace = None

        self.prototype_name = None

        self.prototype_template_name = None
        self.prototype_template_path = None

        self.project_template_name = None
        self.project_template_path = None

        self._try_read_environment_file()

    def _build_arg_parser(self):
        parser = argparse.ArgumentParser(description='WordPress theme and plug-in development tool')
        parser.add_argument('actions', choices=['init', 'start', 'stop', 'register_host', 'deregister_host', 'reregister_host', 'clear', 'download', 'install', 'deploy', 'uninstall', 'build_themes', 'enable_multisite', 'complete_multisite'], help='An action to execute')
        parser.add_argument('--debug', dest='debug', action='store_true', help="Enables debug mode")
        parser.add_argument('--force', dest='force', action='store_true', help="Forces execution of some operations")
        parser.add_argument('--workspace', dest='workspace', help="Workspace path (default is current directory)")
        parser.add_argument('--prototype_name', dest='prototype_name', help="Prototype name")
        parser.add_argument('--prototype_template_name', dest='prototype_template_name', help="Prototype template name")
        parser.add_argument('--prototype_template_path', dest='prototype_template_path', help="Path to prototype template")
        parser.add_argument('--project_template_name', dest='project_template_name', help="Prototype template name")
        parser.add_argument('--project_template_path', dest='project_template_path', help="Path to project template")
        parser.add_argument('--clear_volumes', dest='clear_volumes', action='store_true', help="Clear data volumes")
        return parser

    def _try_read_environment_file(self):
        home = expanduser("~")
        environment_file = os.path.join(home, '.gunillarc')

        if os.path.exists(environment_file):
            self.config = configparser.ConfigParser()
            self.config.read(environment_file)

            project_templates = self.config['project_templates'] if 'project_templates' in self.config else {}
            default_project_template = self.config['gunilla']['default_project_template'] if ('gunilla' in self.config) and ('default_project_template' in self.config['gunilla']) else ''
            if default_project_template in project_templates:
                self.project_template_path = project_templates[default_project_template]

            prototype_templates = self.config['prototype_templates'] if 'prototype_templates' in self.config else {}
            default_prototype_template = self.config['gunilla']['default_prototype_template'] if ('gunilla' in self.config) and ('default_prototype_template' in self.config['gunilla']) else ''
            if default_prototype_template in prototype_templates:
                self.prototype_template_path = prototype_templates[default_prototype_template]

    def read_args(self):
        args = self._parser.parse_args()
        self.action = args.actions[0]
        self.debug = args.debug
        self.force = args.force
        self.clear_volumes = args.clear_volumes
        self.workspace = args.workspace

        self.prototype_name = args.prototype_name

        if args.prototype_template_name:
            self.prototype_template_name = args.prototype_template_name
            if args.prototype_template_name not in self.config['prototype_templates']:
                raise ActionException("Unknown prototype template %s" % args.prototype_template_name)
            self.prototype_template_path = self.config['prototype_templates'][args.prototype_template_name]

        if args.prototype_template_path:
            self.prototype_template_path = args.prototype_template_path

        if args.project_template_name:
            self.project_template_name = args.project_template_name
            if args.project_template_name not in self.config['project_templates']:
                raise ActionException("Unknown project template %s" % args.project_template_name)
            self.project_template_path = self.config['project_templates'][args.project_template_name]

        if args.project_template_path:
            self.project_template_path = args.project_template_path

    def print_usage(self):
        self._parser.print_usage()


_environment = Environment()


def environment():
    return _environment
