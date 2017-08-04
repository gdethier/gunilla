from gunilla.exceptions import WorkspaceException, ActionException
from gunilla.workspace import instance


def run():
    try:
        instance().init()
    except WorkspaceException as e:
        raise ActionException(e)
