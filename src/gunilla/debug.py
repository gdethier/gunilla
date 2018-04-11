from gunilla.environment import environment
import traceback


def error(msg, exception=None):
    print(msg)
    if environment().debug:
        print("")
        print(exception)
        traceback.print_exc()
