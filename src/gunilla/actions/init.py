from gunilla.exceptions import ActionException
from gunilla.workspace import instance


def run():
    workspace = instance()
    if workspace.is_configured():
        raise ActionException("Project seems to be already set up")

    workspace.init()
