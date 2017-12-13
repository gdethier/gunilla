import argparse
from gunilla.actions import get_action
from gunilla.debug import error
from gunilla.environment import instance
from gunilla.exceptions import ActionException
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='WordPress theme and plug-in development tool')
    parser.add_argument('actions', nargs=1, help='An action to execute (one of init, start, stop, register_host, deregister_host, reregister_host, clear, install, uninstall, build_themes, enable_multisite, complete_multisite)')
    parser.add_argument('--debug', dest='debug', action='store_true', help="Enables debug mode")
    parser.add_argument('--force', dest='force', action='store_true', help="Forces execution of some operations")
    parser.add_argument('--prototype_name', dest='prototype_name', help="Prototype name")
    parser.add_argument('--prototype_template_path', dest='prototype_template_path', help="Path to prototype template")
    parser.add_argument('--project_template_path', dest='project_template_path', help="Path to project template")

    args = parser.parse_args()
    instance().debug = args.debug
    instance().force = args.force
    instance().prototype_name = args.prototype_name
    instance().prototype_template_path = args.prototype_template_path
    instance().project_template_path = args.project_template_path

    try:
        action = get_action(args.actions[0])
    except ActionException as e:
        error("Unrecognized action", e)
        parser.print_usage()
        sys.exit(2)

    try:
        action()
    except ActionException as e:
        error(e.args[0], e)
        sys.exit(3)
