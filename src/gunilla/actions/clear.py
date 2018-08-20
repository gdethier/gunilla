from gunilla.exceptions import ActionException
from gunilla.infra import infrastructure
from gunilla.workspace import workspace


def run():
    if not workspace().is_configured():
        raise ActionException("Project was not already set up")

    infrastructure().clear()
