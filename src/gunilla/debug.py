from gunilla.environment import instance
import traceback


def error(msg, exception=None):
    print(msg)
    if instance().debug:
        print("")
        print(exception)
        traceback.print_exc()
