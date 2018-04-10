import logging
import os
import sys

from gunilla.actions import get_action
from gunilla.debug import error
from gunilla.environment import instance
from gunilla.exceptions import ActionException

def main():
    environment = instance()
    environment.read_args()

    if environment.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    try:
        action = get_action(environment.action)
    except ActionException as e:
        error("Unrecognized action: {}".format(environment.action), e)
        environment.print_usage()
        sys.exit(2)

    try:
        action()
    except ActionException as e:
        error(e.args[0], e)
        sys.exit(3)
