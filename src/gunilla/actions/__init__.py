from gunilla.exceptions import ActionException
import sys


def get_action(action):
    try:
        action_module = __import__(__name__ + '.' + action, fromlist=[__name__])
        return getattr(action_module, 'run')
    except (ImportError, AttributeError) as e:
        raise ActionException("Unrecognized action", e)
