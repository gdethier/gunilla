from gunilla.exceptions import ActionException
from gunilla.infra import infrastructure
from gunilla.workspace import workspace
from gunilla.environment import environment


def run():
    if not workspace().is_configured():
        raise ActionException("Project was not already set up")

    infrastructure().clear()

    if environment().clear_volumes:
        infrastructure().clear_volumes()
